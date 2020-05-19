import { Component, OnInit, Input, OnChanges, Output, EventEmitter } from '@angular/core';
import { SystemStatus, SystemState } from '../../system-status';
import { ButtonConfiguration } from 'src/app/basic-ui-elements/button/button-config';
import { CardConfiguration, CardStyle } from './../../basic-ui-elements/card/card.component';

@Component({
  selector: 'app-test-execution',
  templateUrl: './test-execution.component.html',
  styleUrls: ['./test-execution.component.scss']
})
export class TestExecutionComponent implements OnInit, OnChanges {
  testExecutionControlCardConfiguration: CardConfiguration;
  startDutTestButtonConfig: ButtonConfiguration;

  @Input() systemStatus: SystemStatus = new SystemStatus();
  @Output() startDutTestEvent: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor() {
    this.testExecutionControlCardConfiguration = new CardConfiguration();
    this.startDutTestButtonConfig = new ButtonConfiguration();
  }

  ngOnInit() {
    this.startDutTestButtonConfig.labelText = 'Start DUT-Test';
    this.testExecutionControlCardConfiguration = {
      shadow: true,
      cardStyle: CardStyle.COLUMN_STYLE,
      labelText: 'Test Execution'
    };
  }

  ngOnChanges(): void {
    this.updateButtonConfigs();
  }

  private updateButtonConfigs() {
    this.startDutTestButtonConfig.disabled = this.systemStatus.state !== SystemState.ready;
    this.startDutTestButtonConfig = Object.assign({}, this.startDutTestButtonConfig);
  }

  startDutTestButtonClicked() {
    this.startDutTestEvent.emit(true);
  }
}
