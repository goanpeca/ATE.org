import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SystemSiteComponent } from './system-site.component';
import { SystemState } from '../system-status';
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('SystemSiteComponent', () => {
  let component: SystemSiteComponent;
  let fixture: ComponentFixture<SystemSiteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemSiteComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemSiteComponent);
    component = fixture.componentInstance;
    component.systemState = SystemState.initialized;
    fixture.detectChanges();
  });

  it('should create site component', () => {
    expect(component).toBeTruthy();
  });

  it('should table show up', () => {
    const doc = fixture.debugElement.nativeElement;
    expect(doc.querySelector('.table')).toBeDefined();
  });

  it('should have elements', () => {
    const doc = fixture.debugElement.nativeElement;
    expect(doc.querySelector('.table')).toBeDefined();

    expect(fixture.nativeElement.querySelectorAll('th')[0]
                                .textContent.trim())
                                .toBe('Type');
    expect(fixture.nativeElement.querySelectorAll('th')[1]
                                .textContent.trim())
                                .toBe('Site ID');
    expect(fixture.nativeElement.querySelectorAll('th')[2]
                                .textContent.trim())
                                .toBe('State');
  });

});
