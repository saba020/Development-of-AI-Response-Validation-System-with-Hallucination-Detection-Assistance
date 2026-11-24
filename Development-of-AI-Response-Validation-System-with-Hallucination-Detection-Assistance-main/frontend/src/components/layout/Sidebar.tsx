import React, { useEffect, useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  CheckSquare,
  FileText,
  History,
  Cpu,
  Database,
  BarChart3,
  Layers,
  Settings,
  HelpCircle,
  ShieldCheck,
  ChevronRight,
  Info,
  X
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  onOpenSettings: () => void;
  onOpenHelp: () => void;
  isBackendConnected: boolean;
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  collapsed,
  onToggleCollapse,
  onOpenSettings,
  onOpenHelp,
  isBackendConnected,
  mobileOpen = false,
  onCloseMobile,
}) => {
  const location = useLocation();

  // User name state
  const [userName, setUserName] = useState('');
  const [nameInput, setNameInput] = useState('');
  const [showNameDialog, setShowNameDialog] = useState(false);

  // Load saved user name
  useEffect(() => {
    const savedName = localStorage.getItem('ai_eval_user_name');
    if (savedName) {
      setUserName(savedName);
    } else {
      setShowNameDialog(true);
    }
  }, []);

  // Save user name
  const handleSaveName = () => {
    const trimmedName = nameInput.trim();
    if (!trimmedName) return;
    localStorage.setItem('ai_eval_user_name', trimmedName);
    setUserName(trimmedName);
    setShowNameDialog(false);
  };

  // Generate initials from user name
  const initials = userName
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('');

  // 10 Total Navigation Items:
  // 1. Dashboard
  // 2. Evaluate Response
  // 3. Evaluation Results
  // 4. Evaluation History
  // 5. Agent Architecture
  // 6. Knowledge Base
  // 7. Analytics & Reports
  // 8. Batch Evaluation
  // 9. Evaluation Settings (Bottom Controls)
  // 10. System Documentation (Bottom Controls)
  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/evaluate', label: 'Evaluate Response', icon: CheckSquare },
    { to: '/evaluations/latest', label: 'Evaluation Results', icon: FileText },
    { to: '/history', label: 'Evaluation History', icon: History },
    { to: '/agents', label: 'Agent Architecture', icon: Cpu },
    { to: '/knowledge-base', label: 'Knowledge Base', icon: Database },
    { to: '/analytics', label: 'Analytics & Reports', icon: BarChart3 },
    { to: '/batch-evaluation', label: 'Batch Evaluation', icon: Layers },
  ];

  const isItemActive = (to: string) => {
    if (to.startsWith('/evaluations')) {
      return location.pathname.startsWith('/evaluations');
    }
    return location.pathname === to;
  };

  const renderNavLinks = (isMobile = false) => (
    <nav className="p-3 space-y-1">
      {navItems.map((item) => {
        const Icon = item.icon;
        const active = isItemActive(item.to);

        return (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={() => {
              if (isMobile && onCloseMobile) {
                onCloseMobile();
              }
            }}
            className={`flex items-center ${
              collapsed && !isMobile ? 'justify-center px-2' : 'gap-3 px-3'
            } py-2.5 rounded-lg text-xs font-semibold transition-all group ${
              active
                ? 'bg-brand-50 text-brand-700 shadow-xs'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
            title={collapsed && !isMobile ? item.label : undefined}
            aria-label={item.label}
          >
            <Icon
              className={`w-4 h-4 shrink-0 transition-colors ${
                active ? 'text-brand-600' : 'group-hover:text-brand-600'
              }`}
            />
            {(!collapsed || isMobile) && <span className="truncate">{item.label}</span>}
          </NavLink>
        );
      })}
    </nav>
  );

  const renderBottomControls = (isMobile = false) => (
    <div className="p-3 border-t border-slate-200 space-y-2 bg-slate-50/50">
      <div className="space-y-0.5">
        {/* Item 9: Evaluation Settings */}
        <button
          type="button"
          onClick={() => {
            onOpenSettings();
            if (isMobile && onCloseMobile) onCloseMobile();
          }}
          className={`w-full flex items-center ${
            collapsed && !isMobile ? 'justify-center px-2' : 'gap-3 px-3'
          } py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-white hover:text-slate-900 transition-colors cursor-pointer`}
          title={collapsed && !isMobile ? 'Evaluation Settings' : undefined}
          aria-label="Evaluation Settings"
        >
          <Settings className="w-4 h-4 shrink-0 text-slate-500 hover:text-slate-700" />
          {(!collapsed || isMobile) && <span className="truncate">Evaluation Settings</span>}
        </button>

        {/* Item 10: System Documentation */}
        <button
          type="button"
          onClick={() => {
            onOpenHelp();
            if (isMobile && onCloseMobile) onCloseMobile();
          }}
          className={`w-full flex items-center ${
            collapsed && !isMobile ? 'justify-center px-2' : 'gap-3 px-3'
          } py-2 rounded-lg text-xs font-medium text-slate-600 hover:bg-white hover:text-slate-900 transition-colors cursor-pointer`}
          title={collapsed && !isMobile ? 'System Documentation' : undefined}
          aria-label="System Documentation"
        >
          <HelpCircle className="w-4 h-4 shrink-0 text-slate-500 hover:text-slate-700" />
          {(!collapsed || isMobile) && <span className="truncate">System Documentation</span>}
        </button>
      </div>

      {/* Environment Status Badge */}
      {(!collapsed || isMobile) ? (
        <div className="p-2.5 rounded-lg bg-white border border-slate-200 text-[11px]">
          <div className="flex items-center justify-between font-semibold text-slate-700">
            <span className="flex items-center gap-1.5 truncate">
              <span
                className={`w-2 h-2 rounded-full shrink-0 ${
                  isBackendConnected
                    ? 'bg-green-500'
                    : 'bg-amber-500 animate-pulse'
                }`}
              />
              <span className="truncate">
                {isBackendConnected ? 'FastAPI Connected' : 'Demo / Simulation Mode'}
              </span>
            </span>
            <Info className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          </div>

          <p className="text-[10px] text-slate-500 mt-1 leading-tight line-clamp-2">
            {isBackendConnected
              ? 'Connected to live Python evaluation service.'
              : 'Local FAISS & Multi-Agent emulation active.'}
          </p>
        </div>
      ) : (
        <div
          className="flex justify-center py-1"
          title={isBackendConnected ? 'FastAPI Connected' : 'Demo / Simulation Mode'}
        >
          <span
            className={`w-2.5 h-2.5 rounded-full ${
              isBackendConnected ? 'bg-green-500' : 'bg-amber-500 animate-pulse'
            }`}
          />
        </div>
      )}

      {/* Dynamic User Profile */}
      <button
        type="button"
        onClick={() => {
          setNameInput(userName);
          setShowNameDialog(true);
        }}
        className={`w-full pt-1 flex items-center ${
          collapsed && !isMobile ? 'justify-center px-1' : 'gap-3 px-2'
        } py-1.5 rounded-lg text-left hover:bg-slate-100 transition-colors cursor-pointer`}
        title="Change user name"
        aria-label="Change user profile name"
      >
        <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-xs">
          {initials || 'U'}
        </div>

        {(!collapsed || isMobile) && (
          <div className="flex flex-col truncate min-w-0">
            <span className="text-xs font-semibold text-slate-900 truncate">
              {userName || 'User'}
            </span>
            <span className="text-[10px] text-slate-500 truncate">
              Technical Evaluator
            </span>
          </div>
        )}
      </button>
    </div>
  );

  return (
    <>
      {/* Mobile Drawer (closed by default, open when mobileOpen is true) */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop Overlay */}
          <div
            className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity duration-200"
            onClick={onCloseMobile}
            aria-hidden="true"
          />

          {/* Drawer Panel */}
          <aside
            className="fixed top-0 left-0 bottom-0 z-50 h-full h-[100dvh] w-72 max-w-[85vw] bg-white border-r border-slate-200 flex flex-col justify-between shadow-2xl animate-in slide-in-from-left duration-200 overflow-y-auto"
            role="dialog"
            aria-modal="true"
            aria-label="Navigation drawer"
          >
            <div>
              <div className="h-16 flex items-center justify-between px-4 border-b border-slate-200">
                <div className="flex items-center gap-3 overflow-hidden">
                  <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white shrink-0 shadow-xs">
                    <ShieldCheck className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-sm font-bold text-slate-900 tracking-tight leading-none">
                    AI Eval Sentinel
                  </span>
                </div>
                <button
                  type="button"
                  onClick={onCloseMobile}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer"
                  title="Close navigation"
                  aria-label="Close navigation"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {renderNavLinks(true)}
            </div>

            {renderBottomControls(true)}
          </aside>
        </div>
      )}

      {/* Desktop Coordinated Flexbox Push Sidebar (visible on screens >= lg) */}
      <aside
        className={`hidden lg:flex shrink-0 h-full bg-white border-r border-slate-200 flex-col justify-between transition-[width] duration-300 ease-in-out z-20 overflow-hidden ${
          collapsed ? 'w-20' : 'w-64'
        }`}
        aria-label="Main navigation"
      >
        <div className="overflow-hidden">
          {/* Brand Header */}
          <div className="h-16 flex items-center justify-between px-4 border-b border-slate-200 shrink-0">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center text-white shrink-0 shadow-xs">
                <ShieldCheck className="w-5 h-5 text-white" />
              </div>

              {!collapsed && (
                <div className="flex flex-col truncate">
                  <span className="text-sm font-bold text-slate-900 tracking-tight leading-none truncate">
                    AI Eval Sentinel
                  </span>
                </div>
              )}
            </div>

            <button
              type="button"
              onClick={onToggleCollapse}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer shrink-0"
              title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
              aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              <ChevronRight
                className={`w-4 h-4 transform transition-transform duration-200 ${
                  collapsed ? '' : 'rotate-180'
                }`}
              />
            </button>
          </div>

          {renderNavLinks(false)}
        </div>

        {renderBottomControls(false)}
      </aside>

      {/* User Name Setup Dialog */}
      {showNameDialog && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
          <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
            <div className="mb-4">
              <h2 className="text-lg font-bold text-slate-900">
                Welcome to AI Eval Sentinel
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Enter your name to personalize your workspace.
              </p>
            </div>

            <input
              type="text"
              value={nameInput}
              onChange={(e) => setNameInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSaveName();
                }
              }}
              placeholder="e.g. Alex Johnson"
              maxLength={50}
              autoFocus
              className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-100"
            />

            <button
              type="button"
              onClick={handleSaveName}
              disabled={!nameInput.trim()}
              className="mt-4 w-full rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors cursor-pointer"
            >
              Continue
            </button>
          </div>
        </div>
      )}
    </>
  );
};
