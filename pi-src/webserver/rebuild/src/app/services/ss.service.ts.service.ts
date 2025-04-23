import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root', // Makes it available app-wide
})
export class SSEService {
  constructor(private zone: NgZone) {}

  // Connect to an SSE stream
  getServerSentEvents(url: string): Observable<any> {
    return new Observable(observer => {
      const eventSource = new EventSource(url);

      eventSource.onmessage = (event) => {
        // Run inside Angular's zone to trigger change detection
        this.zone.run(() => {
          observer.next(JSON.parse(event.data)); // Parse if your SSE sends JSON
        });
      };

      eventSource.onerror = (error) => {
        this.zone.run(() => {
          observer.error(error);
        });
      };

      // Cleanup on unsubscribe
      return () => {
        eventSource.close();
      };
    });
  }
}