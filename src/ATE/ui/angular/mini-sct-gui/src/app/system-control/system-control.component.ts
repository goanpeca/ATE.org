import { CardConfiguration, CardStyle } from './../basic-ui-elements/card/card.component';
import { Component, OnInit, Output, Input, EventEmitter, OnChanges } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';
import { ButtonConfiguration } from '../basic-ui-elements/button/button-config';
import { InputConfiguration } from '../basic-ui-elements/input/input-config';

enum TextLabel {
  LoadLot = 'Load Lot',
  UnloadLot = 'Unload Lot',
  StartDutTest = 'Start DUT-Test',
}
export enum TextColor {
  black = 'black',
  blue = '#0046AD'
}

@Component({
  selector: 'app-system-control',
  templateUrl: './system-control.component.html',
  styleUrls: ['./system-control.component.scss']
})

export class SystemControlComponent implements OnInit, OnChanges {
  systemControlCardConfiguration: CardConfiguration;
  lotCardConfiguration: CardConfiguration;
  loadLotCardConfiguration: CardConfiguration;
  testExecutionControlCardConfiguration: CardConfiguration;

  loadLotButtonConfig: ButtonConfiguration;
  startDutTestButtonConfig: ButtonConfiguration;
  unloadLotButtonConfig: ButtonConfiguration;

  lotNumberInputConfig: InputConfiguration;

  @Input() systemStatus: SystemStatus = new SystemStatus();

  @Output() loadLotEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output() startDutTestEvent: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() unloadLotEvent: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor() {
    this.systemControlCardConfiguration = new CardConfiguration();
    this.lotCardConfiguration = new CardConfiguration();
    this.loadLotCardConfiguration = new CardConfiguration();
    this.testExecutionControlCardConfiguration = new CardConfiguration();


    this.loadLotButtonConfig = new ButtonConfiguration();
    this.startDutTestButtonConfig = new ButtonConfiguration();
    this.unloadLotButtonConfig = new ButtonConfiguration();

    this.lotNumberInputConfig = new InputConfiguration();
  }

  ngOnInit() {
    this.systemControlCardConfiguration.cardStyle = CardStyle.ROW_STYLE;
    this.systemControlCardConfiguration.labelText = 'System Control';

    this.lotCardConfiguration.cardStyle = CardStyle.COLUMN_STYLE;
    this.lotCardConfiguration.labelText = 'Lot Handling';
    this.lotCardConfiguration.shadow = true;

    this.loadLotCardConfiguration.cardStyle = CardStyle.ROW_STYLE;
    this.loadLotCardConfiguration.shadow = false;

    this.testExecutionControlCardConfiguration.cardStyle = CardStyle.COLUMN_STYLE;
    this.testExecutionControlCardConfiguration.labelText = 'Test Execution';
    this.testExecutionControlCardConfiguration.shadow = true;

    this.loadLotButtonConfig.labelText = TextLabel.LoadLot;
    this.startDutTestButtonConfig.labelText = TextLabel.StartDutTest;
    this.unloadLotButtonConfig.labelText = TextLabel.UnloadLot;

    this.lotNumberInputConfig.placeholder = 'Lot Number ...';
    this.lotNumberInputConfig.textColor = TextColor.black;
  }

  ngOnChanges(): void {
    this.updateButtonConfigs();
    this.updateInputConfigs();
  }

  private updateInputConfigs() {
    this.lotNumberInputConfig.disabled = this.systemStatus.state !== SystemState.initialized;
    this.lotNumberInputConfig = Object.assign({}, this.lotNumberInputConfig);
  }

  private updateButtonConfigs() {
    this.loadLotButtonConfig.disabled = this.systemStatus.state !== SystemState.initialized;
    this.loadLotButtonConfig = Object.assign({}, this.loadLotButtonConfig);

    this.startDutTestButtonConfig.disabled = this.systemStatus.state !== SystemState.ready;
    this.startDutTestButtonConfig = Object.assign({}, this.startDutTestButtonConfig);

    this.unloadLotButtonConfig.disabled = this.systemStatus.state !== SystemState.ready;
    this.unloadLotButtonConfig = Object.assign({}, this.unloadLotButtonConfig);
  }

  renderSystemControlComponent() {
    return this.systemStatus.state !== SystemState.error;
  }

  loadLot(lotNumber : string) {
    this.loadLotEvent.emit(lotNumber);
  }

  unloadLot() {
    this.unloadLotEvent.emit(true);
  }

  startDutTest() {
    this.startDutTestEvent.emit(true);
  }
}
