import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status'

@Component({
  selector: 'app-debug',
  templateUrl: './debug.component.html',
  styleUrls: ['./debug.component.scss']
})
export class DebugComponent implements OnInit {

  mySystemState = SystemState;

  states : any = [
    {
      "description": "Connecting",
      "value": this.mySystemState.connecting
    },
    {
      "description" : "Tester initialized",
      "value": this.mySystemState.initialized
    },
    {
      "description" : "Loading Test Program",
      "value" : this.mySystemState.loading
    },
    {
      "description" : "Ready for DUT Test",
      "value" : this.mySystemState.ready
    },
    {
      "description" : "Test Execution",
      "value" : this.mySystemState.testing
    },
    {
      "description" : "Unloading Test Program",
      "value" : this.mySystemState.unloading
    },
    {
      "description": "Error",
      "value": this.mySystemState.error
    }
  ]

  @Output() systemStateEvent: EventEmitter<SystemState> = new EventEmitter<SystemState>()

  setSystemState(state : SystemState)
  {
    this.systemStateEvent.emit(state)
  }

  constructor() { }

  ngOnInit() {
  }

}
