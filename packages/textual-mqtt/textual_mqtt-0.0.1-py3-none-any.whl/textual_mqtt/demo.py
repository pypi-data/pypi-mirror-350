from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Log, Header, Footer, Label, Input, Button
from textual_mqtt import MqttClient, MqttMessageSubscription, MqttConnectionSubscription
from datetime import datetime

class MqttViewer(Container):
    def compose(self) -> ComposeResult:
        yield Log()
        with Horizontal():
            with Horizontal(id="inputs"):
                yield Input(id="topic", placeholder="Topic")
                yield Input(id="payload", placeholder="Payload")
            with Horizontal(id="button"):
                yield Button("Publish")
        yield MqttMessageSubscription("#")

    @on(MqttMessageSubscription.MqttMessageEvent)
    def mqtt_message_handler(self, evt: MqttMessageSubscription.MqttMessageEvent) -> None:
        self.query_one(Log).write_line(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + evt.topic + " " + evt.payload)

    @on(Input.Submitted)
    @on(Button.Pressed)
    def publish(self):
        if len(self.query_one("#topic", Input).value):
            self.query_one(MqttMessageSubscription).publish(self.query_one("#topic", Input).value, self.query_one("#payload", Input).value)

class MqttDemo(App):

    CSS='''
    #new_footer {
        height: 1;
        dock: bottom;
    }

    #mqtt_status {
        width: 24;
        text-align: right;
        background: $footer-background;
        padding-right: 2;
    }

    #button {
        width: auto;
    }

    Input {
        width: 50%;
    }

    Horizontal {
        height: auto;
    }
    '''

    def compose(self) -> ComposeResult:
        yield Header()
        yield MqttClient()
        yield MqttViewer()
        with Horizontal(id="new_footer"):
            with Horizontal(id="new_inner"):
                yield Footer()
            yield Label("🔴 MQTT Disconnected", id="mqtt_status")
        yield MqttConnectionSubscription()

    @on(MqttConnectionSubscription.MqttConnected)
    def on_mqtt_connect(self, evt: MqttConnectionSubscription.MqttConnected):
        self.query_one("#mqtt_status", Label).update("🟢 MQTT Connected")

    @on(MqttConnectionSubscription.MqttDisconnected)
    def on_mqtt_disconnect(self, evt: MqttConnectionSubscription.MqttDisconnected):
        self.query_one("#mqtt_status", Label).update("🔴 MQTT Disconnected")

def main():
    app = MqttDemo()
    app.run()

if __name__ == "__main__":
    main()