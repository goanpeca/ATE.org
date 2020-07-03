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

@Component({
  selector: 'app-system-console',
  templateUrl: './system-console.component.html',
  styleUrls: ['./system-console.component.scss']
})

export class SystemConsoleComponent implements OnInit {
  clearConsoleButtonConfig: ButtonConfiguration;

  private readonly msgs: IConsoleData[] = [];

  constructor(communicationService: CommunicationService) {
    this.clearConsoleButtonConfig = new ButtonConfiguration();
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  private handleServerMessage(serverMessage: any) {
    this.retrieveData(serverMessage);
  }

  ngOnInit() {
    this.clearConsoleButtonConfig.labelText = 'Clear';
    this.clearConsoleButtonConfig.disabled = false;
  }

  private retrieveData(message) {
    if (!message) { return; }

    const jsonMessage = JSON.parse(JSON.stringify(message));

    const _STATE: string = jsonMessage.payload.state;
    const _TOPIC: string = message.topic;
    const mType: string = jsonMessage.payload.type;

    if (!_STATE || !_TOPIC || !mType) {
      return;
    }

    let data: IConsoleData;
    if (mType === MessageTypes.Status) {
      const description: string = mType + ':      ' + _STATE;
      data = this.generateMessage(description, _TOPIC);
    } else if (jsonMessage.type === MessageTypes.Cmd) {
      const description: string = mType + ':     ' + jsonMessage.command;
      data = this.generateMessage(description, _TOPIC);
    } else if (jsonMessage.type === MessageTypes.Testresult) {
      const description: string = mType + ':     ' + jsonMessage.testdata;
      data = this.generateMessage(description, _TOPIC);
    } else { return; }

    this.msgs.push(data);
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
    this.msgs.length = 0;
  }
}

