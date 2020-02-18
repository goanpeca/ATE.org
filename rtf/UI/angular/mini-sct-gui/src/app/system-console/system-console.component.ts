import { Component, OnInit, Input, PipeTransform, Pipe } from '@angular/core';
import {formatDate } from '@angular/common'

@Component({
  selector: 'app-system-dialog',
  templateUrl: './system-console.component.html',
  styleUrls: ['./system-console.component.scss']
})

@Pipe({
  name: "retrieveData",
  pure: true
})
export class SystemConsoleComponent implements OnInit, PipeTransform {
  transform(value: JSON, args?: any): any {
    return this.retrieveData(value)
  }

  retrieveData(message) {
    if (!message) return

    const jsonMessage = JSON.parse(message.payload)

    const _state: string = jsonMessage.state
    const _topic: string = message.topic
    const mType: string = jsonMessage.type

    if (!_state || !_topic || !mType) {
      return
    }

    let _data: ConsoleData;
    if (mType == MessageTypes.Status) {
      const _description: string = mType + ":      " + _state
      _data = this.generateMessage(_state, _description, _topic)
    }
    else if (jsonMessage.type == MessageTypes.Cmd) {
      const _description: string = mType + ":     " + jsonMessage.command
      _data = this.generateMessage(_state, _description, _topic)
    }
    else if (jsonMessage.type == MessageTypes.Testresult) {
      const _description: string = mType + ":     " + jsonMessage.testdata
      _data = this.generateMessage(_state, _description, _topic)
    }
    else { return }

    this.msgs.push(_data)
  }

  generateMessage(state: string, description: string, topic: string): ConsoleData {
      let _data: ConsoleData = {
        date: formatDate(Date.now(), 'medium', 'en-US'),
        topic: topic,
        description: description
      }

      return _data
  }

  clearConsole() {
    this.msgs.length = 0
  }

  msgs: ConsoleData[] = []
  @Input() msg: JSON


  constructor() {}

  ngOnInit() {}

}

export interface ConsoleData {
  date: string
  topic: string
  description: string
}

export enum MessageTypes {
  Cmd = "cmd",
  Status = "status",
  Testresult = "testresult"
}