import { ComponentFixture, TestBed, async } from '@angular/core/testing';
import { SystemStatusComponent } from './system-status.component';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';
import { CommunicationService } from '../services/communication.service';
import { MockServerService } from '../services/mockserver.service';
import * as constants from '../services/mockserver-constants';
import { waitUntil } from '../test-stuff/auxillary-test-functions';

describe('SystemStatusComponent', () => {
  let component: SystemStatusComponent;
  let fixture: ComponentFixture<SystemStatusComponent>;
  let debugElement: DebugElement;
  let mockServerService: MockServerService;
  let originalJasmineTimeout: number;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemStatusComponent ],
      providers: [ CommunicationService ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    mockServerService = new MockServerService();
    fixture = TestBed.createComponent(SystemStatusComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
    originalJasmineTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
    jasmine.DEFAULT_TIMEOUT_INTERVAL = 10000;
  });

  afterEach( () => {
    jasmine.DEFAULT_TIMEOUT_INTERVAL = originalJasmineTimeout;
    document.getElementById(constants.MOCK_SEVER_SERVICE_NEVER_REMOVABLE_ID).remove();
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });

  it('should show a correct circle color', async () => {

    // condition when we found our green circle
    function foundCircle(color: string): boolean {
      let element = debugElement.query(By.css('span.' + color));
      if (element) {
        return true;
      }
      return false;
    }

    let spy = spyOn<any>(component, 'changeState').and.callThrough();

    // send initialized message
    mockServerService.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_INITIALIZED]);

    let success = await waitUntil(
      () => {
        fixture.detectChanges();
        component.ngOnInit();
      },
      () => foundCircle('green'),
      300,
      6000);

    expect(success).toBeTruthy();
    expect(spy).toHaveBeenCalled();

    // send error message
    mockServerService.setMessages([constants.MESSAGE_WHEN_SYSTEM_STATUS_ERROR]);

    success = await waitUntil(
      () => {
        fixture.detectChanges();
        component.ngOnInit();
      },
      () => foundCircle('red'),
      300,
      6000);

    expect(success).toBeTruthy();
    expect(spy).toHaveBeenCalled();
  });

});
