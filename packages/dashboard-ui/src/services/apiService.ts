import {
  registerAdapters,
  getMsgChannelSelector,
  type MsgProviderAdapter,
} from '@actdim/msgmesh/adapters';
import { DashboardApiClient } from '../api/client';
import { dashboardBus, type DashboardChannelPrefix } from '../bus';
import { FullDashboardData } from '../types';

/**
 * Service Provider wrapping NSwag DashboardApiClient via standard MsgMesh dynamic adapters.
 */
export class DashboardApiService {
  private static instance: DashboardApiService | null = null;
  private sseSource: EventSource | null = null;

  static start() {
    if (!this.instance) {
      this.instance = new DashboardApiService();
      this.instance.registerAdapter();
      this.instance.connectSSE();
    }
    return this.instance;
  }

  private registerAdapter() {
    const services: Record<DashboardChannelPrefix, any> = {
      'API.DASHBOARD.': new DashboardApiClient(),
    };

    const adapters = Object.entries(services).map(
      ([_, service]) =>
        ({
          service,
          channelSelector: getMsgChannelSelector(services),
        }) as MsgProviderAdapter,
    );

    registerAdapters(dashboardBus, adapters);
  }

  private connectSSE() {
    try {
      this.sseSource = new EventSource('/api/events');

      this.sseSource.onopen = () => {
        dashboardBus.send({
          channel: 'APP.SSE.STATUS',
          payload: { connected: true },
        });
      };

      this.sseSource.addEventListener('reload', async () => {
        console.log('[SSE] File change detected -> reloading dashboard data via MsgMesh...');
        try {
          const res = await fetch('/api/data');
          if (res.ok) {
            const data: FullDashboardData = await res.json();
            dashboardBus.send({
              channel: 'APP.DATA.UPDATED',
              payload: data,
            });
          }
        } catch (err) {
          console.error('[SSE] Failed refreshing data:', err);
        }
      });

      this.sseSource.onerror = () => {
        dashboardBus.send({
          channel: 'APP.SSE.STATUS',
          payload: { connected: false },
        });
      };
    } catch {
      dashboardBus.send({
        channel: 'APP.SSE.STATUS',
        payload: { connected: false },
      });
    }
  }
}
