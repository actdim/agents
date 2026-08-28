import React from 'react';
import cytoscape from 'cytoscape';
import {
  type ComponentStruct,
  type ComponentDef,
  type ComponentParams,
  type Component,
  type ComponentModel,
} from '@actdim/dynstruct/componentModel/contracts';
import { useComponent, toReact } from '@actdim/dynstruct/componentModel/react/hooks';
import { Icon } from '@iconify/react';
import { DashboardAppMsgStruct, DashboardMsgChannels } from '../bus';

export type GraphViewStruct = ComponentStruct<
  DashboardAppMsgStruct,
  {
    props: {
      graphData: {
        nodes: Array<{ id: string; label: string; type: string; [key: string]: any }>;
        edges: Array<{ source: string; target: string; type: string; label?: string }>;
      };
    };
    msgScope: {
      publish: DashboardMsgChannels<'APP.ENTITY.SELECT'>;
    };
    actions: {
      resetLayout: () => void;
      fit: () => void;
      zoomIn: () => void;
      zoomOut: () => void;
      selectNode: (id: string) => void;
    };
  }
>;

export const useGraphView = (
  params?: ComponentParams<GraphViewStruct>
): Component<GraphViewStruct> => {
  let c: Component<GraphViewStruct>;
  let m: ComponentModel<GraphViewStruct>;
  let cyInstance: cytoscape.Core | null = null;
  const containerRef = { current: null as HTMLDivElement | null };

  const initCytoscape = () => {
    if (!containerRef.current || !m.graphData) return;

    const elements: cytoscape.ElementDefinition[] = [];

    (m.graphData.nodes || []).forEach((n) => {
      let color = '#38bdf8';
      let shape: cytoscape.Css.NodeShape = 'round-rectangle';

      if (n.type === 'issue') {
        if (n.status === 'done') color = '#10b981';
        else if (n.status === 'in-progress') color = '#f59e0b';
        else if (n.status === 'blocked') color = '#ef4444';
        else color = '#64748b';
      } else if (n.type === 'milestone') {
        color = '#818cf8';
        shape = 'hexagon';
      } else if (n.type === 'risk') {
        color = '#f43f5e';
        shape = 'diamond';
      }

      elements.push({
        data: {
          id: n.id,
          label: n.label,
          color: color,
          shape: shape,
        },
      });
    });

    (m.graphData.edges || []).forEach((e) => {
      let edgeColor = '#475569';
      if (e.type === 'blocks') edgeColor = '#ef4444';
      if (e.type === 'belongs_to') edgeColor = '#38bdf8';
      elements.push({
        data: {
          id: `${e.source}->${e.target}`,
          source: e.source,
          target: e.target,
          label: e.label || '',
          color: edgeColor,
        },
      });
    });

    if (cyInstance) {
      cyInstance.destroy();
    }

    cyInstance = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(color)',
            label: 'data(label)',
            color: '#f8fafc',
            'font-size': '11px',
            'font-family': 'ui-monospace, monospace',
            'text-valign': 'center',
            'text-halign': 'center',
            shape: 'data(shape)' as any,
            width: 'label',
            height: '34px',
            padding: '10px',
            'border-width': 1,
            'border-color': 'rgba(255, 255, 255, 0.2)',
          },
        },
        {
          selector: 'edge',
          style: {
            width: 2,
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            label: 'data(label)',
            'font-size': '9px',
            'font-family': 'ui-monospace, monospace',
            color: '#94a3b8',
            'text-rotation': 'autorotate',
          },
        },
      ],
      layout: {
        name: 'cose',
        padding: 40,
        animate: false,
      } as any,
    });

    cyInstance.on('tap', 'node', (evt) => {
      m.selectNode(evt.target.id());
    });
  };

  const def: ComponentDef<GraphViewStruct> = {
    regType: 'GraphView',
    props: {
      graphData: { nodes: [], edges: [] },
    },
    actions: {
      resetLayout: () => {
        if (cyInstance) {
          cyInstance.layout({ name: 'cose', padding: 40, animate: true } as any).run();
        }
      },
      fit: () => {
        if (cyInstance) {
          cyInstance.fit(undefined, 30);
        }
      },
      zoomIn: () => {
        if (cyInstance) {
          cyInstance.zoom(cyInstance.zoom() * 1.25);
        }
      },
      zoomOut: () => {
        if (cyInstance) {
          cyInstance.zoom(cyInstance.zoom() * 0.8);
        }
      },
      selectNode: (id: string) => {
        c.msgBus.send({
          channel: 'APP.ENTITY.SELECT',
          payload: { id },
        });
      },
    },
    events: {
      onLayoutReady: () => {
        initCytoscape();
      },
      onChangeGraphData: () => {
        initCytoscape();
      },
      onDestroy: () => {
        if (cyInstance) {
          cyInstance.destroy();
          cyInstance = null;
        }
      },
    },
    view: () => (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-sm relative h-[720px] flex flex-col">
        {/* Controls Overlay Bar */}
        <div className="absolute top-4 left-4 z-10 flex items-center gap-2 bg-slate-950/90 backdrop-blur-md p-1.5 rounded-xl border border-slate-800 shadow-lg">
          <button
            onClick={() => m.resetLayout()}
            className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-xs font-medium text-slate-200 rounded-lg transition flex items-center gap-1.5"
            title="Recalculate Layout"
          >
            <Icon icon="lucide:refresh-cw" className="w-3.5 h-3.5" /> Layout
          </button>
          <button
            onClick={() => m.fit()}
            className="px-2.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-xs font-medium text-slate-200 rounded-lg transition"
            title="Fit to Screen"
          >
            <Icon icon="lucide:maximize-2" className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => m.zoomIn()}
            className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 rounded-lg transition"
            title="Zoom In"
          >
            <Icon icon="lucide:zoom-in" className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => m.zoomOut()}
            className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-200 rounded-lg transition"
            title="Zoom Out"
          >
            <Icon icon="lucide:zoom-out" className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Legend Overlay */}
        <div className="absolute bottom-4 left-4 z-10 bg-slate-950/90 backdrop-blur-md p-3 rounded-xl border border-slate-800 text-[10px] font-mono space-y-1.5 shadow-lg">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded bg-emerald-500" /> Done Issue
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded bg-amber-500" /> In-Progress Issue
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded bg-slate-500" /> Open Issue
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded bg-indigo-400" /> Milestone (Hex)
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded bg-rose-500" /> Risk (Diamond)
          </div>
        </div>

        {/* Canvas Container */}
        <div
          ref={(el) => {
            containerRef.current = el;
          }}
          className="w-full h-full cursor-grab active:cursor-grabbing"
        />
      </div>
    ),
  };

  c = useComponent(def, params ?? {});
  m = c.model;
  return c;
};

export const DAGGraphView = toReact(useGraphView);
