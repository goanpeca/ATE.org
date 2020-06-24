import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ButtonComponent } from './../basic-ui-elements/button/button.component';
import { SystemConsoleComponent, IConsoleData } from './system-console.component';
import { DebugElement, NO_ERRORS_SCHEMA } from '@angular/core';

describe('SystemConsoleComponent', () => {
  let msg: IConsoleData;
  let component: SystemConsoleComponent;
  let fixture: ComponentFixture<SystemConsoleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemConsoleComponent, ButtonComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemConsoleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create console component', () => {
    expect(component).toBeTruthy();
  });

  it('should has console', () => {
    const doc = fixture.debugElement.nativeElement;
    expect(doc.querySelector('.scroll_dialog')).toBeDefined();
  });

  it('should has console elements', () => {
    const doc = fixture.debugElement.nativeElement;
    expect(doc.querySelector('table')).toBeDefined();

    expect(fixture.nativeElement.querySelectorAll('th')[0]
                                .textContent.trim())
                                .toBe('Date');
    expect(fixture.nativeElement.querySelectorAll('th')[1]
                                .textContent.trim())
                                .toBe('Topic');
    expect(fixture.nativeElement.querySelectorAll('th')[2]
                                .textContent.trim())
                                .toBe('Description');

  });

  it('should show new elements', () => {
    const doc = fixture.nativeElement;
    msg = {
      date: '01.01.1993',
      topic: 'ATE',
      description: 'status: Idle'
    };

    component.msgs.push(msg);
    fixture.detectChanges();
    expect(doc.querySelectorAll('td')[0]
              .textContent.trim())
              .toBe('01.01.1993');
    expect(doc.querySelectorAll('td')[1]
              .textContent.trim())
              .toBe('ATE');
    expect(doc.querySelectorAll('td')[2]
              .textContent.trim())
              .toBe('status: Idle');
  });
});
