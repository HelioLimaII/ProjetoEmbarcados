"use client";

import { useEffect, useState } from "react";
import { Package, Wifi, WifiOff, ScanLine, AlertTriangle, Clock, CheckCircle2, History } from "lucide-react";

interface ScanData {
  code: string;
  found: boolean;
  product_name?: string;
  message?: string;
  timestamp?: string;
}

export default function Dashboard() {
  const [lastScan, setLastScan] = useState<ScanData | null>(null);
  const [scanHistory, setScanHistory] = useState<ScanData[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const newScan = {
        ...data,
        timestamp: new Date().toLocaleTimeString('pt-BR') // Adiciona a hora exata da leitura
      };
      
      setLastScan(newScan);
      // Adiciona ao histórico e mantém apenas os últimos 5
      setScanHistory(prev => [newScan, ...prev].slice(0, 5));
    };

    return () => ws.close();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 p-4 md:p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Cabeçalho */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 rounded-2xl shadow-sm border border-slate-200 gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">EstoqueManager</h1>
            <p className="text-slate-500 font-medium mt-1">Monitoramento de Scanner em Tempo Real</p>
          </div>
          <div className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-bold text-sm transition-colors ${isConnected ? 'bg-emerald-100 text-emerald-700 border border-emerald-200' : 'bg-rose-100 text-rose-700 border border-rose-200'}`}>
            {isConnected ? <Wifi size={18} /> : <WifiOff size={18} className="animate-pulse" />}
            {isConnected ? "Sistema Online" : "Desconectado"}
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Área Principal - Último Scan (Ocupa 2 colunas) */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
            <div className="p-4 bg-slate-100/50 border-b border-slate-200 flex items-center gap-2">
              <ScanLine size={18} className="text-slate-500" />
              <h2 className="font-semibold text-slate-700">Leitura Atual</h2>
            </div>
            
            <div className="flex-1 p-8 flex flex-col items-center justify-center min-h-[400px]">
              {!lastScan ? (
                <div className="flex flex-col items-center text-slate-400 space-y-6">
                  <div className="p-8 bg-slate-100 rounded-full animate-pulse">
                    <ScanLine size={64} className="text-slate-400" />
                  </div>
                  <p className="text-xl font-medium text-slate-500">Aguardando câmera da ESP-CAM...</p>
                </div>
              ) : (
                <div className={`w-full max-w-lg p-10 rounded-3xl border-2 transition-all duration-500 transform scale-100 ${lastScan.found ? 'border-emerald-400 bg-emerald-50 shadow-emerald-100 shadow-xl' : 'border-rose-400 bg-rose-50 shadow-rose-100 shadow-xl'}`}>
                  <div className="flex flex-col items-center text-center space-y-6">
                    
                    {lastScan.found ? (
                      <>
                        <div className="bg-emerald-500 p-6 rounded-2xl text-white shadow-lg shadow-emerald-200">
                          <Package size={56} strokeWidth={1.5} />
                        </div>
                        <div>
                          <h2 className="text-3xl font-extrabold text-emerald-900 leading-tight">{lastScan.product_name}</h2>
                          <p className="text-emerald-700 font-mono mt-3 bg-emerald-100/50 py-1 px-3 rounded-lg inline-block text-lg border border-emerald-200">
                            {lastScan.code}
                          </p>
                        </div>
                        <div className="flex items-center gap-2 bg-emerald-600 text-white px-6 py-2 rounded-full font-bold shadow-md">
                          <CheckCircle2 size={20} />
                          Estoque Atualizado!
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="bg-rose-500 p-6 rounded-2xl text-white shadow-lg shadow-rose-200">
                          <AlertTriangle size={56} strokeWidth={1.5} />
                        </div>
                        <div>
                          <h2 className="text-3xl font-extrabold text-rose-900 leading-tight">Produto Desconhecido</h2>
                          <p className="text-rose-700 font-mono mt-3 bg-rose-100/50 py-1 px-3 rounded-lg inline-block text-lg border border-rose-200">
                            {lastScan.code}
                          </p>
                          <p className="text-rose-600 font-medium mt-4 bg-white/50 p-3 rounded-xl">{lastScan.message}</p>
                        </div>
                      </>
                    )}

                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar - Histórico de Scans */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col h-full max-h-[500px] lg:max-h-none">
            <div className="p-4 bg-slate-100/50 border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History size={18} className="text-slate-500" />
                <h2 className="font-semibold text-slate-700">Últimas Leituras</h2>
              </div>
              <span className="text-xs font-bold bg-slate-200 text-slate-600 px-2 py-1 rounded-md">{scanHistory.length}</span>
            </div>
            
            <div className="p-4 overflow-y-auto flex-1">
              {scanHistory.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-3">
                  <Clock size={32} className="opacity-50" />
                  <p className="text-sm">Nenhum histórico ainda</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {scanHistory.map((scan, index) => (
                    <div key={index} className={`p-4 rounded-xl border flex items-start gap-3 transition-all ${scan.found ? 'bg-emerald-50/50 border-emerald-100' : 'bg-rose-50/50 border-rose-100'}`}>
                      <div className="mt-1">
                        {scan.found ? <CheckCircle2 size={18} className="text-emerald-500" /> : <AlertTriangle size={18} className="text-rose-500" />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`font-bold truncate ${scan.found ? 'text-emerald-900' : 'text-rose-900'}`}>
                          {scan.found ? scan.product_name : 'Desconhecido'}
                        </p>
                        <p className={`text-xs font-mono truncate ${scan.found ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {scan.code}
                        </p>
                      </div>
                      <div className="text-xs font-medium text-slate-400 whitespace-nowrap">
                        {scan.timestamp}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}