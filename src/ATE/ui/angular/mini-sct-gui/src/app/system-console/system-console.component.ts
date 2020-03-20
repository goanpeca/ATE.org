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
  msgs: ConsoleData[] = [];
  @Input() msg: JSON;
  // tslint:disable-next-line: no-any
  transform(value: JSON, args?: any) {
    this.retrieveData(value);
  }

  retrieveData(message) {
    // abort
    if (!message) { return; }

    const JSON_MESSAGE = JSON.parse(message.payload);

    const STATE: string = JSON_MESSAGE.state;
    const TOPIC: string = message.topic;
    const TYPE: string = JSON_MESSAGE.type;

    if (!STATE || !TOPIC || !TYPE) {
      return;
    }

    let data: ConsoleData;

    if (TYPE === MessageTypes.Status) {
      const description: string = TYPE + ':      ' + STATE;
      data = this.generateMessage(STATE, description, TOPIC);
    } else if (JSON_MESSAGE.type === MessageTypes.Cmd) {
      const description: string = TYPE + ':     ' + JSON_MESSAGE.command;
      data = this.generateMessage(STATE, description, TOPIC);
    } else if (JSON_MESSAGE.type === MessageTypes.Testresult) {
      const description: string = TYPE + ':     ' + JSON_MESSAGE.testdata;
      data = this.generateMessage(STATE, description, TOPIC);
    } else { return; }
    this.msgs.push(data);
  }

  generateMessage(state: string, description: string, topic: string): ConsoleData {

    const DATA: ConsoleData = {
      date: formatDate(Date.now(), 'medium', 'en-US'),
      topic,
      description
    };

    return DATA;
  }

  clearConsole() {
    this.msgs.length = 0;
  }

  constructor() {}

  ngOnInit() {}

}

export interface ConsoleData {
  date: string;
  topic: string;
  description: string;
}

export enum MessageTypes {
  Cmd = 'cmd',
  Status = 'status',
  Testresult = 'testresult'
}
