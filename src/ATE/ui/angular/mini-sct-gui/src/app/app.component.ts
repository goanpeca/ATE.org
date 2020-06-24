import { CommunicationService } from './services/websocket/communication.service';
import { Component } from '@angular/core';
import { SystemStatus, SystemState } from './system-status';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  systemStatus: SystemStatus;

  msg: JSON;
  isSubscribed = false;
  sites: string[] = [];

  sessionCache: object;

constructor(private readonly communicationService: CommunicationService) {
  this.systemStatus = new SystemStatus();
  this.systemStatus.state = SystemState.connecting;

  communicationService.message.subscribe((msg: any) => {
    this.handleServerMessage(msg);

    if (msg.type === 'status') {
      this.setSystemStatus(msg.payload);
    } else if (msg.type === 'testresults') {
      this.addTesttesults(msg.payload);
    } else if (msg.type === 'mqtt.onmessage') {
      this.onMqttProxyMessage(msg.payload);
    }

    console.log('Session id is: ' + this.getSessionId());
  });
}

private handleServerMessage(serverMessage: any) {
  if (serverMessage.payload.state) {
    if (this.systemStatus.state !== serverMessage.payload.state) {
      this.systemStatus.state = serverMessage.payload.state;
    }
  }
}

  systemStateEventChange(event) {
    this.systemStatus.state = event;
    this.systemStatus = Object.assign({}, this.systemStatus);
  }

  getSessionId() {
    const result = localStorage.getItem('sctSessionId');
    if ( result === null ) {
        localStorage.clear();
        localStorage.setItem('sctSessionId', '0' );
    }
    return localStorage.getItem('sctSessionId');
  }

  setSystemStatus(json) {

   this.systemStatus.update(json);

    // make a new instance of system state in order to detect changes by angular
   let copySystemStatus = new SystemStatus();
   this.systemStatus = Object.assign(copySystemStatus, this.systemStatus);
   this.systemStatus = copySystemStatus;

   if (this.isSubscribed) { return; }
   this.initMqttProxy();
   this.isSubscribed = true;
   this.sites = this.systemStatus.sites;

    // Uncomment the following line to publish something with the mqqt proxy
   this.mqttPublish('TEST/angularwebui_setSystemStatus', json, 1);
  }

  addTesttesults(siteidtoarrayoftestresultsdicts) {
    // for (... in ...) statements must be filtered with an if statement (forin)
    // tslint:disable-next-line: forin
    for (const siteid in siteidtoarrayoftestresultsdicts) {
      const arrayoftestresultsdicts = siteidtoarrayoftestresultsdicts[siteid];
      for (const testresult of arrayoftestresultsdicts) {
        console.log('got testresult for site', siteid, ': ', testresult);
      }
    }
  }

  setSessionId(id) {
    localStorage.setItem('sctSessionId', '' + id);
  }

  initMqttProxy() {
    // Uncomment the following line to enable the mqtt proxy with a subscription to all topics
    this.mqttSubscribe('ate/' + this.systemStatus.deviceId + '/#');
  }

  onMqttProxyMessage(message) {
    this.msg = message;
  }

  mqttSubscribe(topic: string, qos: number= 0) {
    this.communicationService.send({type: 'mqtt.subscribe', payload: { topic, qos } });
  }

  mqttPublish(topic: string, payload: object, qos: number= 0, retain: boolean= true) {
    this.communicationService.send({type: 'mqtt.publish', payload: { topic, payload, retain } });
  }
}

