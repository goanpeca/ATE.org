import { Component, OnInit } from '@angular/core';
import { SystemState } from '../../system-status';
import { ButtonConfiguration } from 'src/app/basic-ui-elements/button/button-config';
import { CardConfiguration, CardStyle } from './../../basic-ui-elements/card/card.component';
import { InputConfiguration } from './../../basic-ui-elements/input/input-config';
import { CommunicationService } from './../../services/websocket/communication.service';

enum ButtonTextLabel {
  LoadLot = 'Load Lot',
  UnloadLot = 'Unload Lot'
}

@Component({
  selector: 'app-lot-handling',
  templateUrl: './lot-handling.component.html',
  styleUrls: ['./lot-handling.component.scss']
})
export class LotHandlingComponent implements OnInit {
  lotCardConfiguration: CardConfiguration;

  lotNumberInputConfig: InputConfiguration;

  loadLotButtonConfig: ButtonConfiguration;
  unloadLotButtonConfig: ButtonConfiguration;

  systemState: SystemState;

  constructor(private readonly communicationService: CommunicationService) {
    this.lotCardConfiguration = new CardConfiguration();

    this.lotNumberInputConfig = new InputConfiguration();

    this.loadLotButtonConfig = new ButtonConfiguration();
    this.unloadLotButtonConfig = new ButtonConfiguration();

    this.systemState = SystemState.connecting;
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }
  private handleServerMessage(serverMessage: any) {
    if (serverMessage.payload.state) {
      if (this.systemState !== serverMessage.payload.state) {
        this.systemState = serverMessage.payload.state;
        this.updateButtonConfigs();
        this.updateInputConfigs();
      }
    }
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
    this.updateButtonConfigs();
    this.updateInputConfigs();
  }

  private updateInputConfigs() {
    this.lotNumberInputConfig.disabled = this.systemState !== SystemState.initialized;
    this.lotNumberInputConfig = Object.assign({}, this.lotNumberInputConfig);
  }

  private updateButtonConfigs() {
    this.loadLotButtonConfig.disabled = this.systemState !== SystemState.initialized;
    this.loadLotButtonConfig = Object.assign({}, this.loadLotButtonConfig);

    this.unloadLotButtonConfig.disabled = this.systemState !== SystemState.ready;
    this.unloadLotButtonConfig = Object.assign({}, this.unloadLotButtonConfig);
  }

  loadLot() {
    this.sendLotNumber();
  }

  sendLotNumber() {
    let errorMsg = {errorText: ''};
    if (this.validateLotNumber(errorMsg)) {
      this.communicationService.send(
        {
          type: 'cmd',
          command: 'load',
          lot_number: this.lotNumberInputConfig.value
      });
    } else {
      this.lotNumberInputConfig.errorMsg = errorMsg.errorText;
    }
  }

  unloadLot() {
    this.communicationService.send({type: 'cmd', command: 'unload'});
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
