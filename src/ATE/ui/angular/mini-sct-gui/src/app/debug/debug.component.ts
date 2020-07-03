import { Component, OnInit } from '@angular/core';
import { SystemState } from '../system-status';
import { MockServerService } from '../services/mockserver.service';
import * as constants from '../services/mockserver-constants';

@Component({
  selector: 'app-debug',
  templateUrl: './debug.component.html',
  styleUrls: ['./debug.component.scss']
})
export class DebugComponent implements OnInit {

  mySystemState = SystemState;
  state: any;

  private readonly STATES: any = [
    {
      description: 'Connecting',
      value: this.mySystemState.connecting
    },
    {
      description : 'Tester initialized',
      value: this.mySystemState.initialized
    },
    {
      description : 'Loading Test Program',
      value : this.mySystemState.loading
    },
    {
      description : 'Ready for DUT Test',
      value : this.mySystemState.ready
    },
    {
      description : 'Test Execution',
      value : this.mySystemState.testing
    },
    {
      description : 'Unloading Test Program',
      value : this.mySystemState.unloading
    },
    {
      description: 'Error',
      value: this.mySystemState.error
    }
  ];

  constructor(private readonly mss: MockServerService) {
  }

  ngOnInit() {
  }

  setSystemState(state: SystemState) {
    switch (state) {
      case SystemState.connecting:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_CONNECTING]);
        break;
      case SystemState.initialized:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_INITIALIZED]);
        break;
      case SystemState.ready:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_READY]);
        break;
      case SystemState.loading:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_LOADING]);
        break;
      case SystemState.testing:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_TESTING]);
        break;
      case SystemState.error:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_ERROR]);
        break;
      case SystemState.unloading:
        this.mss.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_UNLOADING]);
        break;
    }
  }
}
