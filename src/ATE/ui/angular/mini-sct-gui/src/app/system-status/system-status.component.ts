import { Component, OnInit } from '@angular/core';
import { SystemState } from '../system-status';
import { CommunicationService } from '../services/communication.service';

export enum Colors {
  red = 'red',
  yellow = 'yellow',
  green = 'green'
}

class RenderedState {
  description: string;
  value: SystemState;
  color: Colors;

  constructor() {
    this.description = '';
    this.value = SystemState.connecting;
    this.color = Colors.yellow;
  }
}

@Component({
  selector: 'app-system-status',
  templateUrl: './system-status.component.html',
  styleUrls: ['./system-status.component.scss']
})

export class SystemStatusComponent implements OnInit {
  private readonly states: Array<RenderedState>;
  private currentState: SystemState;
  private renderedState: RenderedState;

  constructor(private readonly communicationService: CommunicationService) {
    this.states = [
      {
        description: 'Connecting',
        value: SystemState.connecting,
        color: Colors.yellow
      },
      {
        description : 'Tester initialized',
        value: SystemState.initialized,
        color: Colors.green
      },
      {
        description : 'Loading Test Program',
        value : SystemState.loading,
        color: Colors.yellow
      },
      {
        description : 'Ready for DUT Test',
        value : SystemState.ready,
        color: Colors.green
      },
      {
        description : 'Test Execution',
        value : SystemState.testing,
        color: Colors.red
      },
      {
        description : 'Test paused',
        value : SystemState.paused,
        color: Colors.yellow
      },
      {
        description : 'Unloading Test Program',
        value : SystemState.unloading,
        color: Colors.yellow
      },
      {
        description: 'Error',
        value: SystemState.error,
        color: Colors.red
      }
    ];

    this.currentState = SystemState.connecting;
    this.updateRenderedState();
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  private handleServerMessage(serverMessage: any) {
    if (serverMessage && serverMessage.payload && serverMessage.payload.state) {
      if (this.stateChanged(serverMessage.payload.state)) {
        this.changeState(serverMessage.payload.state);
      }
    }
  }

  private updateRenderedState(): void {
    this.renderedState = this.states.filter(s => s.value === this.currentState)[0];
  }

  private stateChanged(receivedState: SystemState): boolean {
    return this.currentState !== receivedState;
  }

  private changeState(state: SystemState) {
    this.currentState = state;
    this.updateRenderedState();
  }

  ngOnInit() {
  }
}
