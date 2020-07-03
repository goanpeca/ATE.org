import { CommunicationService } from './../services/communication.service';
import { SystemState } from './../system-status';
import { CardConfiguration, CardStyle } from './../basic-ui-elements/card/card.component';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-system-control',
  templateUrl: './system-control.component.html',
  styleUrls: ['./system-control.component.scss']
})

export class SystemControlComponent implements OnInit {
  systemControlCardConfiguration: CardConfiguration;

  systemState: SystemState;

  constructor(private readonly communicationService: CommunicationService) {
    this.systemControlCardConfiguration = new CardConfiguration();

    this.systemState = SystemState.connecting;
    communicationService.message.subscribe(msg => this.handleServerMessage(msg));
  }

  private handleServerMessage(serverMessage: any) {
    if (serverMessage.payload.state) {
      if (this.systemState !== serverMessage.payload.state) {
        this.systemState = serverMessage.payload.state;
      }
    }
  }

  ngOnInit() {
    this.systemControlCardConfiguration.cardStyle = CardStyle.ROW_STYLE;
    this.systemControlCardConfiguration.labelText = 'System Control';
  }

  renderSystemControlComponent() {
    return this.systemState !== SystemState.error;
  }
}
