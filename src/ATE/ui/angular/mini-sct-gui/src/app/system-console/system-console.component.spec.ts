import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ButtonComponent } from './../basic-ui-elements/button/button.component';
import { SystemConsoleComponent, IConsoleData } from './system-console.component';
import { DebugElement } from '@angular/core';
import { MockServerService } from './../services/mockserver.service';
import * as constants from '../services/mockserver-constants';
import { By } from '@angular/platform-browser';
import { waitUntil } from './../test-stuff/auxillary-test-functions';

describe('SystemConsoleComponent', () => {
  let msg: IConsoleData;
  let component: SystemConsoleComponent;
  let fixture: ComponentFixture<SystemConsoleComponent>;
  let debugElement: DebugElement;
  let mockServerService: MockServerService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemConsoleComponent, ButtonComponent ],
      providers: [],
      schemas: []
    })
    .compileComponents();
  }));

  beforeEach(() => {
    mockServerService = new MockServerService();
    fixture = TestBed.createComponent(SystemConsoleComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  afterEach( () => {
    document.getElementById(constants.MOCK_SEVER_SERVICE_NEVER_REMOVABLE_ID).remove();
  });

  it('should create console component', () => {
    expect(component).toBeDefined();
  });

  it('should have "clear" button', async(() => {
    const buttons = debugElement.queryAll(By.css('app-button'));
    const clearButtons = buttons.filter(b => b.nativeElement.innerText === 'Clear');
    expect(clearButtons.length).toBe(1, 'There should be a unique button with label text "Clear"');
  }));

  it('should show a table with columns "Date", "Topic" and "Description"', () => {
    const expectedTableHeaders = ['Date', 'Topic', 'Description'];
    let currentTableHeaders = [];
    const ths = debugElement.queryAll(By.css('table th'));

    ths.forEach(h => currentTableHeaders.push(h.nativeElement.innerText));
    expect(currentTableHeaders).toEqual(jasmine.arrayWithExactContents(expectedTableHeaders));
  });

  it('should show message from server', async () => {

    const expectedEntry = [
      constants.TEST_APP_MESSAGE_SITE_7_TESTING.topic,
      'status: ' + constants.TEST_APP_MESSAGE_SITE_7_TESTING.payload.state
    ];

    function entryFound(row: Array<string>): boolean {
      let rows = [];
      debugElement.queryAll(By.css('tr'))
        .filter(
          r => {
            let rowElements = [];
            r.queryAll(By.css('.topic, .description')).forEach(e => rowElements.push(e.nativeElement.innerText));
            rows.push(rowElements);
          }
      );

      return rows.filter( r => JSON.stringify(r) === JSON.stringify(row)).length > 0;
    }

    // configure the mock server to send the following message
    let spy = spyOn<any>(component, 'handleServerMessage').and.callThrough();

    expect(entryFound(expectedEntry)).toBeFalsy('At the beginning there is no entry with "status, testing"');

    // mock some server message
    mockServerService.setMessages([
      constants.TEST_APP_MESSAGE_SITE_7_TESTING,
    ]);

    let success = await waitUntil(
      () => {
        component.ngOnInit();
        fixture.detectChanges();
      },
      () => entryFound(expectedEntry),
      300,
      2000);

    expect(success).toBeTruthy('Entry with "' + JSON.stringify(expectedEntry) + '" must be shown');

    // message handler funtion should have been called
    expect(spy).toHaveBeenCalled();

  });
});

