import { Component, Output, EventEmitter } from '@angular/core';
import { SystemStatus } from './system-status';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  title : string = 'MiniSCT';
  webSocket : WebSocket
  systemStatus : SystemStatus = new SystemStatus()
  msg: JSON;
  is_subscribed: boolean = false;
  sites: string[] = []
  
 

  lotNumberChange(event) {
    this.sendData({
      "type":"cmd",
      "command":"load",
      "lot_number":event
    })
  }

  startDutTestEventChange(event) {
    this.sendData({
      "type":"cmd",
      "command":"next"
    })
  }

  unLoadTestProgramEventChange(event) {
    this.sendData({
      "type":"cmd",
      "command":"unload"
    })
  }

  systemStateEventChange(event) {
    this.systemStatus.state = event;
  }

  sendData(json : object) {
    console.log("Sending json: " + json)
    this.webSocket.send(JSON.stringify(json))
  }

  sessionCache : object;

  getSessionId() {
    var result = localStorage.getItem("sctSessionId");
    if ( result === null )
    {
        localStorage.clear();
        localStorage.setItem("sctSessionId", "0" );
    } 
    return localStorage.getItem("sctSessionId");
  }

  setSystemStatus(json)
  {
    this.systemStatus.update(json)
    if (this.is_subscribed) return
    this.initMqttProxy();
    this.is_subscribed = true
    this.sites = this.systemStatus.sites

    // Uncomment the following line to publish something with the mqqt proxy
    // this.mqttPublish('TEST/angularwebui_setSystemStatus', json, 1)
  }

  addTesttesults(siteidtoarrayoftestresultsdicts)
  {
    for (let siteid in siteidtoarrayoftestresultsdicts) {
      let arrayoftestresultsdicts = siteidtoarrayoftestresultsdicts[siteid];
      for (let testresult of arrayoftestresultsdicts)
      {
        console.log("got testresult for site", siteid, ": ", testresult)
      }
    }
  }
 
  setSessionId(id) {
    localStorage.setItem("sctSessionId", '' + id);
  }

  initMqttProxy()
  {
    // Uncomment the following line to enable the mqtt proxy with a subscription to all topics
    this.mqttSubscribe("ate/" + this.systemStatus.device_id + "/#")
  }

  onMqttProxyMessage(message)
  {
    this.msg = message
  }

  mqttSubscribe(topic:string, qos:number=0)
  {
    this.sendData({type: 'mqtt.subscribe', payload: { topic: topic, qos: qos } });
  }

  mqttPublish(topic:string, payload:object, qos:number=0, retain: boolean=true)
  {
    this.sendData({type: 'mqtt.publish', payload: { topic: topic, payload: payload, retain: retain } });
  }

  constructor() {

    var _self = this;

    this.webSocket = new WebSocket("ws://" + location.host + "/ws");

    this.webSocket.onopen = function (e)
    {
      console.log("WebSocket connection successfully opened")
      _self.sendData({"session": parseInt(_self.getSessionId(), 10)})
    }
    
    this.webSocket.onerror = function (e)
    {
        console.log( "WebSocket connection caused error. type: " + e.type )
    }

    this.webSocket.onclose = function (e)
    {
        console.log( "WebSocket connection has been closed" );
    }

    this.webSocket.onmessage = function (e)
    {
      console.log(e.data + "typeof e.data: " + typeof e.data)
      if ( typeof (e.data) === 'string' ) {
        var jsonMessage = JSON.parse( e.data )
        console.log("WebSocket connection received json: " + JSON.stringify(jsonMessage) )
        if (jsonMessage.type === "status")
        {
          _self.setSystemStatus(jsonMessage.payload)
        }
        else if (jsonMessage.type === "testresults")
        {
          _self.addTesttesults(jsonMessage.payload)
        }
        else if (jsonMessage.type === "mqtt.onmessage")
        {
          _self.onMqttProxyMessage(jsonMessage.payload)
        }
      } else if ( e.data instanceof ArrayBuffer ) {
            console.log( "WebSocket connection received ArrayBuffer" );
      } else if ( e.data instanceof Blob ) {
            console.log("WebSocket connection received Blob" )
      } else {
            console.log( "WebSocket connection something else: " + e.data )
      }

      console.log("Session id is: " + _self.getSessionId())
    };
  }
}

