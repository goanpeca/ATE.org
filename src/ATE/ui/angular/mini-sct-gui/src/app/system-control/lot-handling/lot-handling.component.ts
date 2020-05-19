import { Component, OnInit, Input, OnChanges, EventEmitter, Output } from '@angular/core';
import { SystemStatus, SystemState } from '../../system-status';
import { ButtonConfiguration } from 'src/app/basic-ui-elements/button/button-config';
import { CardConfiguration, CardStyle } from './../../basic-ui-elements/card/card.component';
import { InputConfiguration } from './../../basic-ui-elements/input/input-config';

enum ButtonTextLabel {
  LoadLot = 'Load Lot',
  UnloadLot = 'Unload Lot'
}

@Component({
  selector: 'app-lot-handling',
  templateUrl: './lot-handling.component.html',
  styleUrls: ['./lot-handling.component.scss']
})
export class LotHandlingComponent implements OnInit, OnChanges {
  lotCardConfiguration: CardConfiguration;

  lotNumberInputConfig: InputConfiguration;

  loadLotButtonConfig: ButtonConfiguration;
  unloadLotButtonConfig: ButtonConfiguration;

  @Input() systemStatus: SystemStatus = new SystemStatus();
  @Output() loadLotEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output() unloadLotEvent: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor() {
    this.lotCardConfiguration = new CardConfiguration();

    this.lotNumberInputConfig = new InputConfiguration();

    this.loadLotButtonConfig = new ButtonConfiguration();
    this.unloadLotButtonConfig = new ButtonConfiguration();

  }

  ngOnInit() {
    this.loadLotButtonConfig.labelText = ButtonTextLabel.LoadLot;
    this.unloadLotButtonConfig.labelText = ButtonTextLabel.UnloadLot;

    this.lotNumberInputConfig.placeholder = 'Enter Lot Number';

    this.lotCardConfiguration = {
      shadow: true,
      cardStyle: CardStyle.COLUMN_STYLE,
      labelText: 'Lot Handling'
    };
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

    this.unloadLotButtonConfig.disabled = this.systemStatus.state !== SystemState.ready;
    this.unloadLotButtonConfig = Object.assign({}, this.unloadLotButtonConfig);
  }

  loadLot() {
    this.sendLotNumber();
  }

  sendLotNumber() {
    let errorMsg = {errorText: ''};
    if (this.validateLotNumber(errorMsg)) {
      this.loadLotEvent.emit(this.lotNumberInputConfig.value);
    } else {
      this.lotNumberInputConfig.errorMsg = errorMsg.errorText;
    }
  }

  unloadLot() {
    this.unloadLotEvent.emit(true);
  }

  private validateLotNumber(errorMsg: {errorText: string}): boolean {
    let pattern = /^[1-9][0-9]{5}[.][0-9]{3}$/ ;

    if (pattern.test(this.lotNumberInputConfig.value)) {
      // valid lot number format
      errorMsg.errorText = '';
      return true;
    } else {
      errorMsg.errorText = 'A lot number should be in 6.3 format like \"123456.123\"';
      return false;
    }
  }
}
