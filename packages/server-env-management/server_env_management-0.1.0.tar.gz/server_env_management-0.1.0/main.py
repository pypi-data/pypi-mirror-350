from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits, Label, Static, Input, Checkbox, RadioSet, RadioButton, RichLog
from textual.containers import *
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
import yaml
import docker
import os
import traceback
from io import StringIO
import subprocess as sp
import pandas as pd
import re

def get_gpu_info(queries):
    gpu_info_bytes = sp.check_output(f"nvidia-smi --query-gpu={','.join(queries)} --format=csv".split())
    gpu_info_df = pd.read_csv(StringIO(gpu_info_bytes.decode('utf-8')))
    gpu_info_df = gpu_info_df.rename(columns={col: re.sub(r'\[.*\]', '', col).replace('.', '_').strip() for col in gpu_info_df})
    gpu_info_df = gpu_info_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return gpu_info_df

class Profiles():
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as f:
            self.yaml_profiles = yaml.load(f, Loader=yaml.FullLoader)
    
    def add(self, username, profile):
        if username in self.yaml_profiles:
            return False
        else:
            self.yaml_profiles[username] = profile
            self.flush()
            return True
    
    def edit(self, username, profile):
        if username in self.yaml_profiles:
            self.yaml_profiles[username] = profile
            self.flush()
            return True
        else:
            return False
    
    def remove(self, username):
        if username in self.yaml_profiles:
            del self.yaml_profiles[username]
            self.flush()
            return True
        else:
            return False
        
    def flush(self):
        with open(self.path, 'w') as f:
            yaml.dump(self.yaml_profiles, f, default_flow_style=False, sort_keys=False, )

    def items(self):
        return self.yaml_profiles.items()

    def keys(self):
        return self.yaml_profiles.keys()

class ConfirmScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label('Proceed?', id='question'),
            HorizontalGroup(
                Button('No', id='no'),
                Button('Yes', id='yes'),
            )
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'yes':
            self.dismiss(True)
        if event.button.id == 'no':
            self.dismiss(False)

class ProfileEdit(ModalScreen[dict]):
    BINDINGS = [
        ("escape", " dismiss(None)", "Pop screen"),
        ("q", "dismiss(None)", "Pop screen"),
        ]
    
    def __init__(self, username, profile, default_mode, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.profile = profile
        self.default_mode = default_mode

    def compose(self) -> ComposeResult:
        
        yield HorizontalGroup(
            Label('Editing mode  : ' ),
            RadioSet(
                RadioButton('Add New profile', id='add'),
                RadioButton('Edit Existing profile', id='edit')
            )
        )
        yield HorizontalGroup(
            Label('Username      : ' ),
            Input(id='username')
        )
        yield HorizontalGroup(
            Label('Image Ver.    : '),
            Input(default_image_version, id='image_version')
        )
        yield HorizontalGroup(
            Label('Dataset Dir.  : '),
            Input(default_dataset_dir, id='dataset_dir')
        )
        yield HorizontalGroup(
            Label('Workspace Dir.: '),
            Input(default_workspace_dir, id='workspace_dir')
        )
        yield HorizontalGroup(
            Label('Assigned GPUs : '),
            HorizontalScroll(id='gpu_checkboxes'),
        )  
        yield HorizontalGroup(
            Label('Port Mapping  : '),
            VerticalScroll(
                VerticalGroup(id='port_mappings'),
                HorizontalGroup(
                    Button('+', id='add_port_mapping'),
                    Button('-', id='remove_port_mapping')
                )
                
            ),
            id='port_mapping_group'
        )
        yield HorizontalGroup(
            Button('Exit', id='exit'),
            Button('Save', id='save')
        )
        

    def on_mount(self):

        for i in gpu_info.index:
            self.query_one('#gpu_checkboxes').mount(
                Checkbox(label=f'{i}', id=f'gpu_{i}')
            )

        if self.default_mode == 'add':
            self.query_one('#add').value = True
        elif self.default_mode == 'edit':
            self.query_one('#edit').value = True

        self.query_one('#username').value = self.username

        if self.profile is not None:
            if self.profile['Image Version'] is not None:
                self.query_one('#image_version').value = self.profile['Image Version']
            if self.profile['Dataset Dir'] is not None:
                self.query_one('#dataset_dir').value = self.profile['Dataset Dir']
            if self.profile['Workspace Dir'] is not None:
                self.query_one('#workspace_dir').value = self.profile['Workspace Dir']
            if self.profile['Port Mappings'] is not None:
                for port_mapping in self.profile['Port Mappings']:
                    self.query_one('#port_mappings').mount(Input(port_mapping, placeholder='{container_port}/protocol:{host_port}'))
            if self.profile['GPUs'] is not None:
                for gpu in self.profile['GPUs']:
                    gpu_checkbox = self.query_one(f'#gpu_{gpu}')
                    if gpu_checkbox is not None:
                        gpu_checkbox.value = True


    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'save':
            output = {
                'override': self.query_one('#edit').value,
                'username': self.query_one('#username').value,
                'profile': {
                    'Image Version': self.query_one('#image_version').value,
                    'Dataset Dir': self.query_one('#dataset_dir').value,
                    'Workspace Dir': self.query_one('#workspace_dir').value,
                    'Port Mappings': [port_mapping.value for port_mapping in self.query_one('#port_mappings').children if port_mapping.value != ''],
                    'GPUs': [i for i in range(2) if self.query_one(f'#gpu_{i}').value is True]
                }
            }
            self.dismiss(output)
        
        if event.button.id == 'exit':
            self.dismiss(None)

        if event.button.id == 'add_port_mapping':
            self.query_one('#port_mappings').mount(Input(placeholder='{container_port}/protocol:{host_port}'))
        if event.button.id == 'remove_port_mapping':
            port_mappings = self.query_one('#port_mappings').children
            
            if len(port_mappings) > 0:
                port_mappings[-1].remove()


class ProfileDisplay(HorizontalGroup):

    def __init__(self, username, profile=None, container_info=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.profile = profile
        self.container_info = container_info

    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
            VerticalGroup(
                Label(id='username'),
                Label(id='image_version'),
                Label(id='port_mappings'),
                Label(id='gpus'),

            ),
            Button('Edit', id='edit'),
            Button('Remove', id='remove'),
            Button('Deploy->', id='deploy'),
            id='profile_group',
        )

        yield HorizontalGroup(
            VerticalGroup(
                Label(id='env_name'),
                Label(id='env_status'),
                Label(id='occupied_gpus')
            ),
            Button('Start', id='start'),
            Button('Stop', id='stop'),
            Button('Withdraw', id='withdraw'),
            id='container_group'
        )

        

    def on_mount(self):

        if self.profile is not None:
            self.query_one('#username').update(f'[b]Username:      {self.username}[/b]')
            self.query_one('#image_version').update(f'Image Version: {self.profile["Image Version"]}')
            self.query_one('#port_mappings').update(f'Port Mappings: {self.profile["Port Mappings"][0] if len(self.profile["Port Mappings"]) > 0 else ""}{" [i]etc.[/i]" if len(self.profile["Port Mappings"]) > 1 else ""}')
            self.query_one('#gpus').update(f'Assigned GPUs: {", ".join([str(i) for i in self.profile["GPUs"]])}')
        
        if self.profile is None:
            self.query_one('#edit').disabled = True
            self.query_one('#remove').disabled = True
            self.query_one('#deploy').disabled = True

        if self.container_info is not None:
            self.query_one('#env_name').update(f'Name  : {self.container_info["name"]}')
            self.query_one('#env_status').update(f'Status: {self.container_info["status"]}')
            self.query_one('#occupied_gpus').update(f'GPUs  : {", ".join([str(i) for i in self.container_info["gpus"]])}')

            self.query_one('#remove').disabled = True
            self.query_one('#deploy').disabled = True

            if self.container_info['status'] == 'created':
                self.query_one('#stop').disabled = True

            if self.container_info['status'] == 'running':
                self.query_one('#start').disabled = True
                self.query_one('#withdraw').disabled = True

            if self.container_info['status'] == 'restarting':
                self.query_one('#start').disabled = True
                self.query_one('#withdraw').disabled = True

            if self.container_info['status'] == 'exited':
                self.query_one('#stop').disabled = True

            if self.container_info['status'] == 'paused':
                self.query_one('#withdraw').disabled = True
        
        if self.container_info is None:
            self.query_one('#start').disabled = True
            self.query_one('#stop').disabled = True
            self.query_one('#withdraw').disabled = True

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'edit':
            self.app.action_edit_profile(self.username, self.profile, 'edit')
        if event.button.id == 'remove':
            self.app.action_remove_profile(self.username)
        if event.button.id == 'deploy':
            try:
                container = client.containers.run(
                    image=f'maxium0526/server-env:{self.profile["Image Version"]}',
                    name=f'SERVER_ENV_{self.username}',
                    device_requests=[ # --gpus
                        docker.types.DeviceRequest(
                            capabilities=[['gpu']],
                            device_ids=[str(i) for i in self.profile['GPUs']]
                            )
                        ],
                    volumes=[
                        f'{os.path.join(self.profile["Dataset Dir"], self.username)}:/datasets',
                        f'{os.path.join(self.profile["Workspace Dir"], self.username)}:/workspace',
                    ],
                    ports={f'{port_mapping.split(":")[0]}': f'{port_mapping.split(":")[1]}' for port_mapping in self.profile['Port Mappings']},
                    labels={
                        'username': self.username,
                        'gpus': ','.join([str(i) for i in self.profile['GPUs']]),
                    },
                    environment=[f'ENV_USERNAME={self.username}'],
                    restart_policy={"Name": "always"},
                    shm_size='128G',
                    detach=True,
                    stdin_open=True, # -it
                    tty=True, # -it
                    init=True,
                )
                container.start()
            except Exception:
                self.app.query_one(RichLog).write(traceback.format_exc())

            self.app.refresh_profile_displays()

        if event.button.id == 'start':
            try:
                container = client.containers.get(self.container_info['id'])
                container.start()
            except Exception:
                self.app.query_one(RichLog).write(traceback.format_exc())
            self.app.refresh_profile_displays()

        if event.button.id == 'restart':
            try:
                container = client.containers.get(self.container_info['id'])
                container.restart()
            except Exception:
                self.app.query_one(RichLog).write(traceback.format_exc())
            self.app.refresh_profile_displays()

        if event.button.id == 'stop':
            self.app.action_stop_container(self.container_info['id'])

        if event.button.id == 'withdraw':
            self.app.action_withdraw_container(self.container_info['id'])

class Home(App):
    CSS_PATH = 'css.tcss'
    BINDINGS = [
        ('a', 'edit_profile("", None, "add")', 'Add profile'),
        ('l', 'trigger_show_log', 'Show/Hide Log'),
        ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id='profiledisplays')
        yield RichLog(id='log', wrap=True)
        yield Footer()

    def on_mount(self):
        self.refresh_profile_displays()

    def action_edit_profile(self, username, profile, mode):
        if self.is_screen_installed('profile_edit'):
            return

        def callback(data: dict):
            if data is not None:
                if data['override'] is True:
                    profiles.edit(data['username'], data['profile'])
                else:
                    profiles.add(data['username'], data['profile'])

            self.refresh_profile_displays()
            self.uninstall_screen('profile_edit')

        self.install_screen(ProfileEdit(username, profile, mode), name='profile_edit')
        self.push_screen('profile_edit', callback=callback)

    def action_remove_profile(self, username):

        def callback(result: bool):
            if result is True:
                profiles.remove(username)
                self.refresh_profile_displays()
            
            self.uninstall_screen('confirm_remove')

        self.install_screen(ConfirmScreen(), name='confirm_remove')
        self.push_screen('confirm_remove', callback=callback)

    def action_stop_container(self, id):

        def callback(result: bool):
            if result is True:
                try:
                    container = client.containers.get(id)
                    container.stop()
                except Exception:
                    self.app.query_one(RichLog).write(traceback.format_exc())
                self.app.refresh_profile_displays()
            
            self.uninstall_screen('confirm_stop')

        self.install_screen(ConfirmScreen(), name='confirm_stop')
        self.push_screen('confirm_stop', callback=callback)

    def action_withdraw_container(self, id):

        def callback(result: bool):
            try:
                container = client.containers.get(id)
                container.remove()
            except Exception:
                self.app.query_one(RichLog).write(traceback.format_exc())
            self.app.refresh_profile_displays()
            
            self.uninstall_screen('confirm_withdraw')

        self.install_screen(ConfirmScreen(), name='confirm_withdraw')
        self.push_screen('confirm_withdraw', callback=callback)

    def action_trigger_show_log(self):
        display = self.query_one(RichLog).display
        if display == True:
            display = self.query_one(RichLog).display = False
        else:
            display = self.query_one(RichLog).display = True

    def refresh_profile_displays(self):
        try:
            containers = [c for c in client.containers.list(all=True) if c.name.startswith('SERVER_ENV_')]
        except Exception:
            self.app.query_one(RichLog).write(traceback.format_exc())

        self.query_one('#profiledisplays').remove_children()
        for username, profile in profiles.items():

            container = [c for c in containers if c.name == f'SERVER_ENV_{username}']
            container = container[0] if len(container) > 0 else None
            
            if container is not None: # collect infromation of the container for showing
                container_info = {
                    'id': container.id,
                    'short_id': container.short_id,
                    'name': container.name,
                    'version': container.image.tags[0].split(':')[-1],
                    'status': container.status,
                    'gpus': [] if 'gpus' not in container.labels or len(container.labels['gpus'])==0 else [int(i) for i in container.labels['gpus'].split(',')],
                }
            else:
                container_info = None

            self.query_one('#profiledisplays').mount(ProfileDisplay(username, profile, container_info=container_info))

        # get the usernames of all profiles
        profile_usernames = list(profiles.keys())
        
        unassociated_containers = [c for c in containers if c.name.split('_')[-1] not in profile_usernames]

        for container in unassociated_containers:

            self.query_one('#profiledisplays').mount(ProfileDisplay('', None,
                container_info={
                    'id': container.id,
                    'short_id': container.short_id,
                    'name': container.name,
                    'version': container.image.tags[0].split(':')[-1],
                    'status': container.status,
                    'gpus': [] if 'gpus' not in container.labels or len(container.labels['gpus'])==0 else [int(i) for i in container.labels['gpus'].split(',')],
                }))

if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    global client, profiles, default_dataset_dir, default_workspace_dir, default_image_version, gpu_info
    if 'Docker Socket' not in config:
        client = docker.from_env()
    else:
        client = docker.DockerClient(config['Docker Socket'])
    profiles = Profiles(config['Profiles'])

    gpu_info = get_gpu_info(['index', 'gpu_name', 'gpu_bus_id'])

    default_dataset_dir = config['Default Dataset Dir']
    default_workspace_dir = config['Default workspace Dir']
    default_image_version = config['Default Image Version']

    app = Home()
    app.run()
    