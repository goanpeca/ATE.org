import { Component, OnInit } from '@angular/core';
import { SystemState } from '../../system-status';
import { ButtonConfiguration } from 'src/app/basic-ui-elements/button/button-config';
import { CardConfiguration, CardStyle } from './../../basic-ui-elements/card/card.component';
import { CommunicationService } from './../../services/websocket/communication.service';

@Component({
  selector: 'app-test-execution',
  templateUrl: './test-execution.component.html',
  styleUrls: ['./test-execution.component.scss']
})
export class TestExecutionComponent implements OnInit {
  testExecutionControlCardConfiguration: CardConfiguration;
  startDutTestButtonConfig: ButtonConfiguration;

  systemState: SystemState;

  constructor(private readonly communicationService: CommunicationService) {
    this.testExecutionControlCardConfiguration = new CardConfiguration();
    this.startDutTestButtonConfig = new ButtonConfiguration();

    this.systemState = SystemState.connecting;
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  private handleServerMessage(serverMessage: any) {
    if (serverMessage.payload.state) {
      if (this.systemState !== serverMessage.payload.state) {
        this.systemState = serverMessage.payload.state;
        this.updateButtonConfigs();
      }
    }
  }

  ngOnInit() {
    this.startDutTestButtonConfig.labelText = 'Start DUT-Test';
    this.testExecutionControlCardConfiguration = {
      shadow: true,
      cardStyle: CardStyle.COLUMN_STYLE,
      labelText: 'Test Execution'
    };
  }

  private updateButtonConfigs() {
    this.startDutTestButtonConfig.disabled = this.systemState !== SystemState.ready;
    this.startDutTestButtonConfig = Object.assign({}, this.startDutTestButtonConfig);
  }

  startDutTest() {
    this.communicationService.send({type: 'cmd', command: 'next'});
  }
}
