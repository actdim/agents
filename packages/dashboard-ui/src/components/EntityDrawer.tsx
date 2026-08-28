import React from 'react';
import {
  type ComponentStruct,
  type ComponentDef,
  type ComponentParams,
  type Component,
  type ComponentModel,
} from '@actdim/dynstruct/componentModel/contracts';
import { useComponent, toReact } from '@actdim/dynstruct/componentModel/react/hooks';
import { type BaseAppMsgStruct } from '@actdim/dynstruct/appDomain/appContracts';
import { useDrawer, type DrawerStruct } from '@actdim/dynstruct-mui/Drawer';
import { bind } from '@actdim/dynstruct/componentModel/core';
import { Icon } from '@iconify/react';
import { marked } from 'marked';
import { FullDashboardData } from '../types';

export type EntityDrawerStruct = ComponentStruct<
  BaseAppMsgStruct,
  {
    props: {
      data: FullDashboardData | null;
      selectedEntityId: string | null;
      onClose: () => void;
      readonly entity: any | null;
      readonly renderedBody: string;
    };
    children: {
      drawer: DrawerStruct;
    };
  }
>;

export const useEntityDrawer = (
  params?: ComponentParams<EntityDrawerStruct>
): Component<EntityDrawerStruct> => {
  let c: Component<EntityDrawerStruct>;
  let m: ComponentModel<EntityDrawerStruct>;

  const def: ComponentDef<EntityDrawerStruct> = {
    regType: 'EntityDrawer',
    props: {
      data: null,
      selectedEntityId: null,
      onClose: () => {},
      get entity() {
        if (!m.data || !m.selectedEntityId) return null;
        const id = m.selectedEntityId;

        const iss = m.data.issues.find((i) => i.id === id || i.slug === id);
        if (iss) return { ...iss, entityType: 'issue' };

        const mil = m.data.milestones.find((ml) => ml.id === id || ml.slug === id);
        if (mil) return { ...mil, entityType: 'milestone' };

        const r = m.data.risks.find((rk) => rk.id === id || rk.slug === id);
        if (r) return { ...r, entityType: 'risk' };

        const sp = m.data.spikes.find((s) => s.id === id || s.slug === id);
        if (sp) return { ...sp, entityType: 'spike' };

        const sess = m.data.sessions.find((s) => s.id === id || s.slug === id);
        if (sess) return { ...sess, entityType: 'session' };

        const kb = m.data.kb_articles.find((k) => k.id === id || k.slug === id);
        if (kb) return { ...kb, entityType: 'kb' };

        const dec = m.data.decisions.find((d) => d.id === id);
        if (dec) return { ...dec, entityType: 'decision', body: dec.raw_markdown };

        return null;
      },
      get renderedBody() {
        const ent = m.entity;
        if (!ent || !ent.body) return '';
        try {
          return marked.parse(ent.body) as string;
        } catch {
          return ent.body;
        }
      },
    },
    children: {
      drawer: useDrawer({
        anchor: 'right',
        open: bind(() => Boolean(m.selectedEntityId)),
        onClose: bind(() => m.onClose),
        children: () => {
          const ent = m.entity;
          if (!ent) return null;

          return (
            <div className="w-full sm:w-[600px] bg-slate-900 text-slate-100 p-6 min-h-screen flex flex-col justify-between">
              <div className="space-y-6">
                {/* Header */}
                <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                  <div>
                    <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-sky-400 border border-slate-700">
                      {ent.entityType}
                    </span>
                    <h2 className="text-xl font-bold text-slate-100 mt-2 tracking-tight">
                      {ent.title || ent.slug || ent.id}
                    </h2>
                    <div className="text-xs text-slate-400 font-mono mt-1">{ent.id}</div>
                  </div>
                  <button
                    onClick={m.onClose}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition"
                    title="Close drawer"
                  >
                    <Icon icon="lucide:x" className="w-5 h-5" />
                  </button>
                </div>

                {/* Metadata Grid */}
                <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-xs font-mono grid grid-cols-2 gap-3 text-slate-400">
                  {ent.status && (
                    <div>
                      Status: <span className="text-slate-200 font-bold uppercase">{ent.status}</span>
                    </div>
                  )}
                  {ent.priority && (
                    <div>
                      Priority: <span className="text-slate-200 font-bold uppercase">{ent.priority}</span>
                    </div>
                  )}
                  {ent.type && (
                    <div>
                      Type: <span className="text-slate-200 font-bold">{ent.type}</span>
                    </div>
                  )}
                  {ent.agent && (
                    <div>
                      Agent: <span className="text-slate-200">{ent.agent}</span>
                    </div>
                  )}
                  {ent.created && (
                    <div>
                      Created: <span className="text-slate-200">{ent.created}</span>
                    </div>
                  )}
                  {ent.completed && (
                    <div>
                      Completed: <span className="text-emerald-400 font-bold">{ent.completed}</span>
                    </div>
                  )}
                  {ent.file_path && (
                    <div className="col-span-2">
                      File: <span className="text-sky-400">{ent.file_path}</span>
                    </div>
                  )}
                </div>

                {/* Tags */}
                {Array.isArray(ent.tags) && ent.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5">
                    {ent.tags.map((t: string) => (
                      <span
                        key={t}
                        className="text-xs font-mono px-2 py-0.5 rounded bg-slate-950 text-slate-400 border border-slate-800"
                      >
                        #{t}
                      </span>
                    ))}
                  </div>
                )}

                {/* Content */}
                <div className="border-t border-slate-800 pt-4">
                  <h3 className="text-xs font-bold font-mono uppercase text-slate-400 mb-3">
                    Description & Content
                  </h3>
                  <div
                    className="markdown-body prose prose-invert max-w-none text-slate-300 text-xs leading-relaxed"
                    dangerouslySetInnerHTML={{
                      __html: m.renderedBody || '<p class="italic text-slate-500">No content provided.</p>',
                    }}
                  />
                </div>
              </div>

              <div className="border-t border-slate-800 pt-4 mt-6 flex justify-end">
                <button
                  onClick={m.onClose}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-medium transition"
                >
                  Close
                </button>
              </div>
            </div>
          );
        },
      }),
    },
    view: () => <c.children.Drawer />,
  };

  c = useComponent(def, params ?? {});
  m = c.model;
  return c;
};

export const EntityDrawer = toReact(useEntityDrawer);
