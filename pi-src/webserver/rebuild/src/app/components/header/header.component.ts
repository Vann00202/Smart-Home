import { Component } from '@angular/core';
import { PrimaryButtonComponent } from "../primary-button/primary-button.component";

@Component({
  selector: 'app-header',
  imports: [PrimaryButtonComponent],
  template: `
  <div class="header">
  
    {{title}}
    <app-primary-button label = 'Turn OFF/ON'/>

  </div>

  `,
  styles: `
  .header{
    background: rgba(0,0,0,.5);
    color: black;
    padding: 1rem;
  }
  `
})


export class HeaderComponent {
  title = 'Wired Living Lights: ';
}
