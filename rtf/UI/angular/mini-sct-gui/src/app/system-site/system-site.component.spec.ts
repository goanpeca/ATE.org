import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemSiteComponent } from './system-site.component';
import { SystemState } from '../system-status';

describe('SystemSiteComponent', () => {
  let component: SystemSiteComponent;
  let fixture: ComponentFixture<SystemSiteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemSiteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemSiteComponent);
    component = fixture.componentInstance;
    component.systemStatus.state = SystemState.initialized
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should table show up', () => {
    const doc = fixture.debugElement.nativeElement
    expect(doc.querySelector('.table')).toBeDefined()
  });

  it('should have elements', () => {
    const doc = fixture.debugElement.nativeElement
    expect(doc.querySelector('.table')).toBeDefined()

    expect(fixture.nativeElement.querySelectorAll("th")[0]
                                .textContent.trim())
                                .toBe("Type")
    expect(fixture.nativeElement.querySelectorAll("th")[1]
                                .textContent.trim())
                                .toBe("Site ID")
    expect(fixture.nativeElement.querySelectorAll("th")[2]
                                .textContent.trim())
                                .toBe("State")
  })

});
