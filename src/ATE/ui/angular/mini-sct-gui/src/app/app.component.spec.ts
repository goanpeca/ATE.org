import { InfomationComponent } from './basic-ui-elements/infomation/infomation.component';
import { CheckboxComponent } from './basic-ui-elements/checkbox/checkbox.component';
import { ButtonComponent } from './basic-ui-elements/button/button.component';
import { InputComponent } from './basic-ui-elements/input/input.component';
import { CardComponent, CardStyle } from './basic-ui-elements/card/card.component';
import { NO_ERRORS_SCHEMA, DebugElement, ChangeDetectionStrategy } from '@angular/core';
import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { SystemStatusComponent } from './system-status/system-status.component';
import { SystemControlComponent } from './system-control/system-control.component';
import { DebugComponent } from './debug/debug.component';
import { SystemConsoleComponent } from './system-console/system-console.component';
import { SystemSiteComponent } from './system-site/system-site.component';
import { HeaderComponent } from './pages/header/header.component';
import { FooterComponent } from './pages/footer/footer.component';
import { SystemState } from './system-status';
import { TestOptionComponent } from './system-control/test-option/test-option.component';

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
        DebugComponent,
        SystemConsoleComponent,
        SystemSiteComponent,
        HeaderComponent,
        FooterComponent,
        CardComponent,
        InputComponent,
        ButtonComponent,
        CheckboxComponent,
        InfomationComponent,
        TestOptionComponent
      ],
        schemas: [NO_ERRORS_SCHEMA]
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

  describe('Tags of the other component type', () => {
    it('should contain an app-header tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-header');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-system-status tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-system-status');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-system-control tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-system-control');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-system-site tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-system-site');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-debug tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-debug');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-system-dialog tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-system-dialog');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-footer tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-footer');
      expect(componentElement).not.toEqual(null);
    }));
  });
});
