import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { DebugElement } from '@angular/core';
import { SystemInformationComponent } from './system-information.component';
import { SystemState, SystemStatus } from '../system-status';
import { By } from '@angular/platform-browser';
import { CardComponent } from '../basic-ui-elements/card/card.component';
import { InformationComponent } from '../basic-ui-elements/information/information.component';
import { MockServerService } from './../services/mockserver.service';
import * as constants from '../services/mockserver-constants';
import { waitUntil } from './../test-stuff/auxillary-test-functions';
import { formatDate } from '@angular/common';

describe('SystemInformationComponent', () => {
  let component: SystemInformationComponent;
  let fixture: ComponentFixture<SystemInformationComponent>;
  let debugElement: DebugElement;
  let systemStatus: SystemStatus;
  let mockServerService: MockServerService;
  let expectedLabelText = ['System', 'Number of Sites', 'Time', 'Environment', 'Handler'];

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [],
      declarations: [ SystemInformationComponent, CardComponent, InformationComponent ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    mockServerService = new MockServerService();
    fixture = TestBed.createComponent(SystemInformationComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    systemStatus = new SystemStatus();
    fixture.detectChanges();
  });

  afterEach( () => {
    document.getElementById(constants.MOCK_SEVER_SERVICE_NEVER_REMOVABLE_ID).remove();
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });

  it('should display "System Information" as label text', () => {
    expect(component.informationCardConfiguration.labelText).toBe('System Information');
  });

  it('should show error messages when system state is ' + JSON.stringify(SystemState.error), () => {
    expect(component.showError()).toBeDefined();

    let errorMsg = 'system has error';
    let errorElement = debugElement.query(By.css('.error h3'));

    if (component.showError()) {
      systemStatus.reason = errorMsg;

      expect(errorElement.nativeElement.textContent).toBe('system has error');
    }
  });

  it('should support hr tag', () => {
    let hrElement = debugElement.nativeElement.querySelector('hr');
    expect(hrElement).toBeTruthy();
  });

  it('should contain 2 app-card tags', () => {
    let cardElement = debugElement.nativeElement.querySelectorAll('app-card');

    expect(cardElement).not.toEqual(null);
    expect(cardElement.length).toBe(2);
  });

  it('current system status is ' + JSON.stringify(SystemState.connecting), () => {
    expect(systemStatus.state).toBe('connecting');
  });

  describe('When system state is ' + JSON.stringify(SystemState.connecting), () => {
    it('should support heading', () => {
      let appCardBody = debugElement.query(By.css(('app-card app-card .card .body')));
      expect(appCardBody.nativeElement.textContent).toBe('Identifying Test System!');
    });

    it('should display labelText "System Identification"', () => {
      let appCardHeader = debugElement.query(By.css(('app-card app-card .card .header')));
      expect(appCardHeader.nativeElement.textContent).toBe('System Identification');
    });
  });

  describe('When system state is neither ' + JSON.stringify(SystemState.connecting) + ' nor ' + JSON.stringify(SystemState.error), () => {
    it('should contain 5 app-information tags', async () => {
      function foundAPPInformation(): boolean {
        let element = debugElement.queryAll(By.css('app-information'));
        if (element.length === 5) {
          return true;
        }
        return false;
      }

      // send initialized message
      mockServerService.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_INITIALIZED]);

      let success = await waitUntil(
        () => {
          fixture.detectChanges();
          component.ngOnInit();
        },
        foundAPPInformation,
        300,
        6000);

      expect(success).toBeTruthy();
    });

    it('should display label texts: ' + JSON.stringify(expectedLabelText), async () => {
      expect(component.infoContentCardConfiguration.labelText).toEqual('');

      function foundLabeTexts(): boolean {
        let element = debugElement.queryAll(By.css('app-information'));
        return element.length === 5;
      }
      // send initialized message
      mockServerService.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_INITIALIZED]);
      let success = await waitUntil(
        () => {
          fixture.detectChanges();
          component.ngOnInit();
        },
        foundLabeTexts,
        300,
        6000);

      let labelElements = [];
      debugElement.queryAll(By.css('app-information h2'))
        .forEach(a => labelElements
          .push(a.nativeElement.innerText));

      expect(success).toBeTruthy();
      expect(labelElements).toEqual(jasmine.arrayWithExactContents(expectedLabelText));
    });

    it('should display value of system information', async () => {
      expect(component.systemInformationConfiguration.value).toEqual('');

      function foundLabeTexts(): boolean {
        let element = debugElement.queryAll(By.css('app-information'));
        if (element.length === 5) {
          return true;
        }
        return false;
      }
      // send testing message
      mockServerService.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_TESTING]);
      let success = await waitUntil(
        () => {
          fixture.detectChanges();
          component.ngOnInit();
        },
        foundLabeTexts,
        300,
        6000);
      expect(success).toBeTruthy();

      let valueTexts = [];
      debugElement.queryAll(By.css('app-information h3'))
        .forEach(a => valueTexts
          .push(a.nativeElement.innerText));

      expect(valueTexts).toEqual(['MiniSCT', formatDate(Date.now(), 'medium', 'en-US'), 'F1', 'invalid']);
    });
  });
});
