import { InformationConfiguration } from './../basic-ui-elements/infomation/information-config';
import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';
import { CardConfiguration, CardStyle } from './../basic-ui-elements/card/card.component';

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
export class SystemStatusComponent implements OnInit, OnChanges {
  @Input() systemStatus: SystemStatus = new SystemStatus();

  protected mySystemState = SystemState;
  // property for error information
  visiable = true;

  informationCardConfiguration: CardConfiguration;
  identifyCardConfiguration: CardConfiguration;
  infoContentCardConfiguration: CardConfiguration;

  sytemInformationConfiguration: InformationConfiguration;
  numberOfSitesConfiguration: InformationConfiguration;
  timeInformationConfiguration: InformationConfiguration;
  environmentInformationConfiguration: InformationConfiguration;
  handlerInformationConfiguration: InformationConfiguration;

  constructor() {
    this.informationCardConfiguration = new CardConfiguration();
    this.identifyCardConfiguration = new CardConfiguration();
    this.infoContentCardConfiguration = new CardConfiguration();

    this.sytemInformationConfiguration = new InformationConfiguration();
    this.numberOfSitesConfiguration = new InformationConfiguration();
    this.timeInformationConfiguration = new InformationConfiguration();
    this.environmentInformationConfiguration = new InformationConfiguration();
    this.handlerInformationConfiguration = new InformationConfiguration();
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

    this.sytemInformationConfiguration.labelText = systemInformationLabelText.systemLabelText;
    this.numberOfSitesConfiguration.labelText = systemInformationLabelText.sitesLabelText;
    this.timeInformationConfiguration.labelText = systemInformationLabelText.timeLabelText;
    this.environmentInformationConfiguration.labelText = systemInformationLabelText.environmentLabelText;
    this.handlerInformationConfiguration.labelText = systemInformationLabelText.handlerLabelText;
  }

  ngOnChanges() {
    console.log('system information app detected change');
    this.updateView();
  }

  updateView() {
    if (this.systemStatus.deviceId) {
      this.sytemInformationConfiguration.value = this.systemStatus.deviceId;
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
