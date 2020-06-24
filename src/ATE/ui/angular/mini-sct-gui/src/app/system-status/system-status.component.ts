import { InformationConfiguration } from './../basic-ui-elements/information/information-config';
import { Component, OnInit } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';
import { CardConfiguration, CardStyle } from './../basic-ui-elements/card/card.component';
import { CommunicationService } from '../services/websocket/communication.service';

export enum systemInformationLabelText {
  systemLabelText = 'System',
  sitesLabelText = 'Number of Sites',
  timeLabelText = 'Time',
  environmentLabelText = 'Environment',
  handlerLabelText = 'Handler'
}

@Component({
  selector: 'app-system-status',
  templateUrl: './system-status.component.html',
  styleUrls: ['./system-status.component.scss']
})
export class SystemStatusComponent implements OnInit {
  protected systemState = SystemState;
  systemStatus: SystemStatus;

  informationCardConfiguration: CardConfiguration;
  identifyCardConfiguration: CardConfiguration;
  infoContentCardConfiguration: CardConfiguration;

  systemInformationConfiguration: InformationConfiguration;
  numberOfSitesConfiguration: InformationConfiguration;
  timeInformationConfiguration: InformationConfiguration;
  environmentInformationConfiguration: InformationConfiguration;
  handlerInformationConfiguration: InformationConfiguration;

  constructor(private readonly communicationService: CommunicationService) {
    this.systemStatus = new SystemStatus();
    this.systemStatus.state = SystemState.connecting;

    this.informationCardConfiguration = new CardConfiguration();
    this.identifyCardConfiguration = new CardConfiguration();
    this.infoContentCardConfiguration = new CardConfiguration();

    this.systemInformationConfiguration = new InformationConfiguration();
    this.numberOfSitesConfiguration = new InformationConfiguration();
    this.timeInformationConfiguration = new InformationConfiguration();
    this.environmentInformationConfiguration = new InformationConfiguration();
    this.handlerInformationConfiguration = new InformationConfiguration();

    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  handleServerMessage(serverMessage: any) {
    if (serverMessage.payload.state) {
      if (this.systemStatus.state  !== serverMessage.payload.state) {
        this.systemStatus.state = serverMessage.payload.state;
        this.systemStatus.update(serverMessage.payload);
        this.updateView();
      }
    }
  }

  showError() {
    return this.systemStatus.state === SystemState.error;
  }

  ngOnInit() {
    this.informationCardConfiguration.cardStyle = CardStyle.ROW_STYLE;
    this.informationCardConfiguration.labelText = 'System Information';

    this.identifyCardConfiguration = {
      shadow: true,
      cardStyle: CardStyle.COLUMN_STYLE,
      labelText: 'System Identification'
    };

    this.infoContentCardConfiguration.cardStyle = CardStyle.COLUMN_STYLE;
    this.infoContentCardConfiguration.shadow = true;

    this.systemInformationConfiguration.labelText = systemInformationLabelText.systemLabelText;
    this.numberOfSitesConfiguration.labelText = systemInformationLabelText.sitesLabelText;
    this.timeInformationConfiguration.labelText = systemInformationLabelText.timeLabelText;
    this.environmentInformationConfiguration.labelText = systemInformationLabelText.environmentLabelText;
    this.handlerInformationConfiguration.labelText = systemInformationLabelText.handlerLabelText;
  }

  updateView() {
    if (this.systemStatus.deviceId) {
      this.systemInformationConfiguration.value = this.systemStatus.deviceId;
    }

    if (this.systemStatus.sites) {
      this.numberOfSitesConfiguration.value = this.systemStatus.sites.length;
    }

    if (this.systemStatus.time) {
      this.timeInformationConfiguration.value = this.systemStatus.time;
    }

    if (this.systemStatus.env) {
      this.environmentInformationConfiguration.value = this.systemStatus.env;
    }

    if (this.systemStatus.handler) {
      this.handlerInformationConfiguration.value = this.systemStatus.handler;
    }
  }
}
