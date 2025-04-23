import { Component,OnDestroy,OnInit } from '@angular/core';
import { PrimaryButtonComponent } from "../primary-button/primary-button.component";
import { ButtonONComponent } from '../button-on/button-on.component';
import { ButtonOFFComponent } from '../button-off/button-off.component';
import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom } from 'rxjs';
import { SSEService } from '../../services/ss.service.ts.service';
import { Subscription } from 'rxjs'

@Component({
  selector: 'app-header',
  imports: [PrimaryButtonComponent, ButtonOFFComponent, ButtonONComponent],
  template: `
  <div class="header">
  
    {{title}}
    {{status}}

  </div>
  <div class="header">
    Light Switch: 
    <app-button-on></app-button-on>
    <app-button-off></app-button-off>
    <app-primary-button label = 'Toggle ON/OFF'/>
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
@Injectable({
  providedIn: 'root'
})

export class HeaderComponent implements OnInit, OnDestroy{
  title = 'Wired Living Lights Status: ';
  status = 'Undetermined';

  private sseSubscription: Subscription | null=null;

  constructor(private sseService: SSEService) {}



  ngOnInit() {
    const sseUrl = 'http://192.168.12.1:3000/sse';

    this.sseSubscription = this.sseService
      .getServerSentEvents(sseUrl)
      .subscribe({
        next: (data) => {
          this.status = data; // Update UI with new data
        },
        error: (err) => {
          console.error('SSE Error:', err);
        },
      });
  }
  ngOnDestroy() {
    // Unsubscribe to avoid memory leaks
    if (this.sseSubscription) {
      this.sseSubscription.unsubscribe();
    }
  }
}
