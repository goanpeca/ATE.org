import { CommunicationService } from './../services/communication.service';
import { Component, OnInit } from '@angular/core';
import {formatDate } from '@angular/common';
import { ButtonConfiguration } from './../basic-ui-elements/button/button-config';

export interface IConsoleData {
  date: string;
  topic: string;
  description: string;
}

export enum MessageTypes {
  Cmd = 'cmd',
  Status = 'status',
  Testresult = 'testresult'
}

let msgs: IConsoleData[] = [];

@Component({
  selector: 'app-system-console',
  templateUrl: './system-console.component.html',
  styleUrls: ['./system-console.component.scss']
})
export class SystemConsoleComponent implements OnInit {
  clearConsoleButtonConfig: ButtonConfiguration;



  constructor(communicationService: CommunicationService) {
    this.clearConsoleButtonConfig = new ButtonConfiguration();
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  private handleServerMessage(serverMessage: any) {
    this.retrieveData(serverMessage);
  }

  getMessages() {
    return msgs;
  }

  ngOnInit() {
    this.clearConsoleButtonConfig.labelText = 'Clear';
    this.clearConsoleButtonConfig.disabled = false;
  }

  private retrieveData(message) {
    if (!message) { return; }

    let payload: any;
    if (message.type === 'mqtt.onmessage') {
      payload = message.payload.payload;
    } else {
      return;
    }

    const _STATE: string = payload.state;
    const _TOPIC: string = message.payload.topic;
    const mType: string = payload.type;

    if (!_STATE || !_TOPIC || !mType) {
      return;
    }

    let data: IConsoleData;
    if (mType === MessageTypes.Status) {
      const description: string = mType + ':      ' + _STATE;
      data = this.generateMessage(description, _TOPIC);
    } else if (message.type === MessageTypes.Cmd) {
      const description: string = mType + ':     ' + message.command;
      data = this.generateMessage(description, _TOPIC);
    } else if (message.type === MessageTypes.Testresult) {
      const description: string = mType + ':     ' + message.testdata;
      data = this.generateMessage(description, _TOPIC);
    } else { return; }

    msgs.push(data);
  }

  generateMessage(description: string, topic: string): IConsoleData {
      const DATA: IConsoleData = {
        date: formatDate(Date.now(), 'medium', 'en-US'),
        topic,
        description
      };
      return DATA;
  }

  clearConsole() {
    msgs.length = 0;
  }
}

