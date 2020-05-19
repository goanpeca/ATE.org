import { Component, OnInit, Input, PipeTransform, Pipe } from '@angular/core';
import {formatDate } from '@angular/common';

@Component({
  selector: 'app-system-dialog',
  templateUrl: './system-console.component.html',
  styleUrls: ['./system-console.component.scss']
})

@Pipe({
  name: 'retrieveData',
  pure: true
})
export class SystemConsoleComponent implements OnInit, PipeTransform {


  constructor() {}

  @Input() msg: JSON;
  msgs: IConsoleData[] = [];
  transform(value: JSON, args?: any): any {
    return this.retrieveData(value);
  }

  retrieveData(message) {
    if (!message) { return; }

    const jsonMessage = JSON.parse(message.payload);

    const _STATE: string = jsonMessage.state;
    const _TOPIC: string = message.topic;
    const mType: string = jsonMessage.type;

    if (!_STATE || !_TOPIC || !mType) {
      return;
    }

    let data: IConsoleData;
    if (mType === MessageTypes.Status) {
      const description: string = mType + ':      ' + _STATE;
      data = this.generateMessage(_STATE, description, _TOPIC);
    } else if (jsonMessage.type === MessageTypes.Cmd) {
      const description: string = mType + ':     ' + jsonMessage.command;
      data = this.generateMessage(_STATE, description, _TOPIC);
    } else if (jsonMessage.type === MessageTypes.Testresult) {
      const description: string = mType + ':     ' + jsonMessage.testdata;
      data = this.generateMessage(_STATE, description, _TOPIC);
    } else { return; }

    this.msgs.push(data);
  }

  generateMessage(state: string, description: string, topic: string): IConsoleData {
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

  ngOnInit() {}

}

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
