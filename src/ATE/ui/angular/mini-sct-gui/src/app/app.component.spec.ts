import { RouterModule } from '@angular/router';
import { CommunicationService } from './services/communication.service';
import { WebsocketService } from './services/websocket.service';
import { InformationComponent } from './basic-ui-elements/information/information.component';
import { CheckboxComponent } from './basic-ui-elements/checkbox/checkbox.component';
import { ButtonComponent } from './basic-ui-elements/button/button.component';
import { InputComponent } from './basic-ui-elements/input/input.component';
import { CardComponent } from './basic-ui-elements/card/card.component';
import { DebugElement } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { SystemStatusComponent } from './system-status/system-status.component';
import { SystemControlComponent } from './system-control/system-control.component';
import { SystemConsoleComponent } from './system-console/system-console.component';
import { SystemSiteComponent } from './system-site/system-site.component';
import { HeaderComponent } from './pages/header/header.component';
import { FooterComponent } from './pages/footer/footer.component';
import { TestOptionComponent } from './system-control/test-option/test-option.component';
import * as constants from './services/mockserver-constants';
import { LotHandlingComponent } from './system-control/lot-handling/lot-handling.component';
import { TestExecutionComponent } from './system-control/test-execution/test-execution.component';
import { SystemInformationComponent } from './system-information/system-information.component';
import { MenuComponent } from './menu/menu.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        SystemStatusComponent,
        SystemControlComponent,
        SystemConsoleComponent,
        SystemSiteComponent,
        SystemInformationComponent,
        HeaderComponent,
        FooterComponent,
        CardComponent,
        InputComponent,
        ButtonComponent,
        CheckboxComponent,
        InformationComponent,
        TestOptionComponent,
        LotHandlingComponent,
        TestExecutionComponent,
        InputComponent,
        MenuComponent,
      ],
      providers: [
        WebsocketService,
        CommunicationService,
      ],
      imports: [FormsModule, RouterTestingModule, RouterModule],
      })
      .compileComponents();
    }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create the miniSCT app', () => {
    expect(component).toBeTruthy();
  });

  it('debug component should not be present in release versions', () => {
    let appDebug = fixture.nativeElement.querySelector('app-debug');
    expect(appDebug).toBeFalsy('Please remove any html element having tag "app-debug" manually. This component is only used during development');
  });

  it('the mockserver-service should not be executed', () => {
   let mockServerElement = document.getElementById(constants.MOCK_SEVER_SERVICE_NEVER_REMOVABLE_ID);
   expect(mockServerElement).toBeFalsy('Please remove any dependency injected MockserverService and any HTML element having tag <app-debug>');
  });

  describe('Tags of the other component type', () => {
    it('should contain an app-header tag', () => {
      let componentElement = debugElement.nativeElement.querySelectorAll('app-header');
      expect(componentElement).not.toEqual(null);
      expect(componentElement.length).toBe(1);
    });

    it('should contain an app-system-status tag', () => {
      let componentElement = debugElement.nativeElement.querySelectorAll('app-system-status');
      expect(componentElement).not.toEqual(null);
      expect(componentElement.length).toBe(1);
    });

    it('should contain an app-menu tag', () => {
      let componentElement = debugElement.nativeElement.querySelectorAll('app-menu');
      expect(componentElement).not.toEqual(null);
      expect(componentElement.length).toBe(1);
    });

    it('should contain an app-footer tag', () => {
      let componentElement = debugElement.nativeElement.querySelectorAll('app-footer');
      expect(componentElement).not.toEqual(null);
      expect(componentElement.length).toBe(1);
    });
  });
});
