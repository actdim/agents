import React from 'react';
import {
  type ComponentStruct,
  type ComponentDef,
  type ComponentParams,
  type Component,
  type ComponentModel,
} from '@actdim/dynstruct/componentModel/contracts';
import { useComponent, toReact } from '@actdim/dynstruct/componentModel/react/hooks';
import { useDialog, type DialogStruct } from '@actdim/dynstruct-mui/Dialog';
import { bind } from '@actdim/dynstruct/componentModel/core';
import { Icon } from '@iconify/react';
import { SearchResultItem, SearchResponse } from '../types';
import { DashboardAppMsgStruct, DashboardMsgChannels } from '../bus';

export type SearchModalStruct = ComponentStruct<
  DashboardAppMsgStruct,
  {
    props: {
      isOpen: boolean;
      onClose: () => void;
      query: string;
      activeTypeFilter: string;
      results: SearchResultItem[];
      loading: boolean;
    };
    msgScope: {
      publish: DashboardMsgChannels<'API.DASHBOARD.SEARCHKB' | 'APP.ENTITY.SELECT'>;
    };
    actions: {
      performSearch: (queryText: string) => Promise<void>;
      selectResult: (r: SearchResultItem) => void;
    };
    children: {
      dialog: DialogStruct;
    };
  }
>;

export const useSearchModal = (
  params?: ComponentParams<SearchModalStruct>
): Component<SearchModalStruct> => {
  let c: Component<SearchModalStruct>;
  let m: ComponentModel<SearchModalStruct>;

  const def: ComponentDef<SearchModalStruct> = {
    regType: 'SearchModal',
    props: {
      isOpen: false,
      onClose: () => {},
      query: '',
      activeTypeFilter: 'all',
      results: [],
      loading: false,
    },
    actions: {
      performSearch: async (queryText: string) => {
        m.query = queryText;
        if (!queryText.trim()) {
          m.results = [];
          return;
        }
        m.loading = true;
        try {
          const typeParam = m.activeTypeFilter === 'all' ? undefined : m.activeTypeFilter;
          const msgResp = await c.msgBus.request({
            channel: 'API.DASHBOARD.SEARCHKB',
            payload: [queryText, undefined, typeParam as any],
          });
          const resp = msgResp.payload;
          m.results = resp?.results || [];
        } catch (err) {
          console.error('Search error:', err);
          m.results = [];
        } finally {
          m.loading = false;
        }
      },
      selectResult: (r: SearchResultItem) => {
        c.msgBus.send({
          channel: 'APP.ENTITY.SELECT',
          payload: { id: r.id, type: r.type },
        });
        m.onClose();
      },
    },
    events: {
      onChangeActiveTypeFilter: () => {
        if (m.query) {
          m.performSearch(m.query);
        }
      },
    },
    children: {
      dialog: useDialog({
        open: bind(() => m.isOpen),
        onClose: bind(() => m.onClose),
        fullWidth: true,
        maxWidth: 'md',
        content: () => (
          <div className="bg-slate-900 text-slate-100 p-0 flex flex-col max-h-[80vh]">
            {/* Search Bar Input */}
            <div className="flex items-center px-4 py-3.5 border-b border-slate-800 gap-3">
              <Icon icon="lucide:search" className="w-5 h-5 text-sky-400 shrink-0" />
              <input
                type="text"
                autoFocus
                value={m.query}
                onChange={(e) => m.performSearch(e.target.value)}
                placeholder="Search across Knowledge Base, Issues, ADR decisions..."
                className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm focus:outline-none"
              />
              {m.loading && (
                <Icon icon="lucide:loader-2" className="w-4 h-4 text-sky-400 animate-spin shrink-0" />
              )}
              <button onClick={m.onClose} className="text-slate-500 hover:text-slate-300 p-1 rounded-lg">
                <Icon icon="lucide:x" className="w-4 h-4" />
              </button>
            </div>

            {/* Filter Pills */}
            <div className="flex items-center gap-1.5 px-4 py-2 bg-slate-950/60 border-b border-slate-800 text-[10px] font-mono">
              <span className="text-slate-500 mr-1">Filter:</span>
              {['all', 'kb', 'issue', 'decision', 'session'].map((t) => (
                <button
                  key={t}
                  onClick={() => {
                    m.activeTypeFilter = t;
                  }}
                  className={`px-2 py-0.5 rounded uppercase ${
                    m.activeTypeFilter === t
                      ? 'bg-sky-600 text-white font-bold'
                      : 'bg-slate-900 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>

            {/* Results List */}
            <div className="overflow-y-auto p-3 space-y-2 flex-1">
              {m.results.map((r) => (
                <div
                  key={r.id}
                  onClick={() => m.selectResult(r)}
                  className="p-3 bg-slate-950 border border-slate-800/80 hover:border-sky-500/50 rounded-xl cursor-pointer transition group"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-mono uppercase px-1.5 py-0.2 rounded bg-slate-900 text-sky-400 border border-slate-800">
                        {r.type}
                      </span>
                      <h4 className="text-xs font-bold text-slate-200 group-hover:text-sky-300 transition">
                        {r.title}
                      </h4>
                    </div>
                    <span className="text-[10px] text-slate-500 font-mono">{r.file_path}</span>
                  </div>
                  {r.snippet && (
                    <p className="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
                      {r.snippet}
                    </p>
                  )}
                </div>
              ))}

              {m.query.trim() && !m.loading && m.results.length === 0 && (
                <div className="py-12 text-center text-xs text-slate-500 font-mono italic">
                  No results found for &ldquo;{m.query}&rdquo;
                </div>
              )}

              {!m.query.trim() && (
                <div className="py-8 text-center text-xs text-slate-500 font-mono">
                  Type to start searching knowledge base topics, issues, decisions, and sessions.
                </div>
              )}
            </div>
          </div>
        ),
      }),
    },
    view: () => <c.children.Dialog />,
  };

  c = useComponent(def, params ?? {});
  m = c.model;
  return c;
};

export const SearchModal = toReact(useSearchModal);
