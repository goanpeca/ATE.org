import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { DebugElement } from '@angular/core';
import { SystemInformationComponent } from './system-information.component';
import { SystemState, SystemStatus } from '../system-status';
import { By } from '@angular/platform-browser';
import { CardComponent } from '../basic-ui-elements/card/card.component';
import { InformationComponent } from '../basic-ui-elements/information/information.component';

describe('SystemInformationComponent', () => {
  let component: SystemInformationComponent;
  let fixture: ComponentFixture<SystemInformationComponent>;
  let debugElement: DebugElement;
  let systemStatus: SystemStatus;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [],
      declarations: [ SystemInformationComponent, CardComponent, InformationComponent ],
      schemas: []
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemInformationComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    systemStatus = new SystemStatus();
    fixture.detectChanges();
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });

  it('should display "System Information" as label text', () => {
    expect(component.informationCardConfiguration.labelText).toBe('System Information');
  });

  it('should show error messages when system state is "error"', () => {
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

  it('current system status is "connecting"', () => {
    expect(systemStatus.state).toBe('connecting');
  });

  describe('When system state is "connecting"', () => {
    it('should support heading', () => {
      let appCardBody = debugElement.query(By.css(('app-card app-card .card .body')));
      expect(appCardBody.nativeElement.textContent).toBe('Identifying Test System!');
    });

    it('should display labelText "System Identification"', () => {
      let appCardHeader = debugElement.query(By.css(('app-card app-card .card .header')));
      expect(appCardHeader.nativeElement.textContent).toBe('System Identification');
    });
  });

  describe('When system state is neither "error" nor "connecting"', () => {
    it('should contain 5 app-information tags', (done) => {

      // set system state to something different from error or connecting, i.e. to ready
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();

      let infoElement = debugElement.nativeElement.querySelectorAll('app-information');
      expect(infoElement.length).toBe(5);
      done();
    });

    it('should display label texts: "System", "Number of Sites", "Time", "Environment", "Handler"', (done) => {
      expect(component.infoContentCardConfiguration.labelText).toEqual('');

      // set system state to something different from error or connecting, i.e. to ready
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();

      let lableElements = debugElement.queryAll(By.css('app-information h2'));

      let labelTexts = [];
      lableElements.forEach( l => labelTexts.push(l.nativeElement.innerText));

      expect(labelTexts).toEqual(jasmine.arrayWithExactContents(['System', 'Number of Sites', 'Time', 'Environment', 'Handler']));
      done();
    });

    it('should display value of system information', (done) => {
      expect(component.systemInformationConfiguration.value).toEqual('');

      // set system state to something different from error or connecting, i.e. to testing
      (component as any).handleServerMessage(
        {
          payload: {
            state: SystemState.testing,
            device_id: 'Test-Id',
            env: 'Test-Environment',
            handler: 'Test-Handler',
            sites: ['Test-Site-A', 'Test-Site-B'],
            systemTime: 'Test-SystemTime'
          }});
      fixture.detectChanges();

      let valueElements = debugElement.queryAll(By.css('app-information h3'));

      let valueTexts = [];
      valueElements.forEach( v => valueTexts.push(v.nativeElement.innerText));

      expect(valueTexts).toEqual(jasmine.arrayWithExactContents(['Test-Id', 'Test-Environment', 'Test-Handler', 'Test-SystemTime']));
      done();
    });
  });
});
