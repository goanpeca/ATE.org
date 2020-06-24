import { CommunicationService } from './services/websocket/communication.service';
import { WebsocketService } from './services/websocket/websocket.service';
import { TestOptionComponent } from './system-control/test-option/test-option.component';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { SystemStatusComponent } from './system-status/system-status.component';
import { SystemControlComponent } from './system-control/system-control.component';
import { DebugComponent } from './debug/debug.component';
import { SystemConsoleComponent } from './system-console/system-console.component';
import { SystemSiteComponent } from './system-site/system-site.component';
import { HeaderComponent } from './pages/header/header.component';
import { FooterComponent } from './pages/footer/footer.component';
import { ButtonComponent } from './basic-ui-elements/button/button.component';
import { InputComponent } from './basic-ui-elements/input/input.component';
import { CardComponent } from './basic-ui-elements/card/card.component';
import { CheckboxComponent } from './basic-ui-elements/checkbox/checkbox.component';
import { InformationComponent } from './basic-ui-elements/information/information.component';
import { LotHandlingComponent } from './system-control/lot-handling/lot-handling.component';
import { TestExecutionComponent } from './system-control/test-execution/test-execution.component';

@NgModule({
  declarations: [
    AppComponent,
    SystemStatusComponent,
    SystemControlComponent,
    DebugComponent,
    SystemConsoleComponent,
    SystemSiteComponent,
    HeaderComponent,
    FooterComponent,
    ButtonComponent,
    InputComponent,
    CardComponent,
    CheckboxComponent,
    InformationComponent,
    TestOptionComponent,
    LotHandlingComponent,
    TestExecutionComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [WebsocketService, CommunicationService],
  bootstrap: [AppComponent]
})
export class AppModule { }
