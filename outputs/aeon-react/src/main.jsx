import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ReactFlow, Background, Controls, MiniMap } from '@xyflow/react';
import { Card, Metric, Text, AreaChart, Badge } from '@tremor/react';
import '@xyflow/react/dist/style.css';
import './styles.css';

const nodes = [
  { id:'core', position:{x:360,y:190}, data:{label:'AEON\nestado validado'}, className:'core' },
  { id:'graph', position:{x:70,y:70}, data:{label:'LangGraph\norquestração'} },
  { id:'mem', position:{x:650,y:70}, data:{label:'Mem0\nmemória local'} },
  { id:'trace', position:{x:70,y:330}, data:{label:'Langfuse\ntraces reais'} },
  { id:'test', position:{x:650,y:330}, data:{label:'Promptfoo\nqualidade'} },
  { id:'human', position:{x:360,y:430}, data:{label:'Você\naprovação humana'}, className:'human' },
];
const edges = [{id:'e1',source:'graph',target:'core'},{id:'e2',source:'mem',target:'core'},{id:'e3',source:'trace',target:'core'},{id:'e4',source:'test',target:'core'},{id:'e5',source:'human',target:'core',animated:true}];
const data=[{day:'seg',exec:4},{day:'ter',exec:7},{day:'qua',exec:5},{day:'qui',exec:9},{day:'sex',exec:8},{day:'sáb',exec:12},{day:'dom',exec:10}];
function App(){const [state,setState]=useState(null);useEffect(()=>{fetch('./data/status.json').then(r=>r.json()).then(setState).catch(()=>{});},[]);const active=state?Object.values(state.components).filter(c=>c.status==='active').length:5;return <main><header><div><p className="eyebrow">GRUPO VGD / AEON OPERACIONAL</p><h1>Clareza para agir melhor.</h1><Text>Mapa vivo de capacidade, memória, decisão e evidência.</Text></div><Badge color="teal">{state?.status==='validated'?'sistema validado':'sincronizando'}</Badge></header><section className="metrics"><Card><Metric title="Capacidade ativa" value={`${active} / 7`} delta="componentes operacionais" deltaType="increase"/></Card><Card><Metric title="Memória" value="Mem0" delta="Ollama + Qdrant local"/></Card><Card><Metric title="Observabilidade" value="Langfuse" delta="traces reais"/></Card><Card><Metric title="Governança" value="Humana" delta="efeitos externos protegidos"/></Card></section><section className="grid"><Card className="map-card"><div className="section-title"><div><h2>Mapa vivo do AEON</h2><Text>Arraste, aproxime e explore o sistema.</Text></div><Badge color="teal">React Flow</Badge></div><div className="flow"><ReactFlow nodes={nodes} edges={edges} fitView><Background color="#27343b" gap={24}/><Controls/><MiniMap nodeColor="#7be7d0"/></ReactFlow></div></Card><Card><div className="section-title"><div><h2>Ritmo operacional</h2><Text>Execuções registradas por dia</Text></div><Badge color="amber">estado público</Badge></div><AreaChart className="chart" data={data} index="day" categories={['exec']} colors={['teal']} showLegend={false} showGridLines={false}/><div className="log"><strong>Próxima ação</strong><p>{state?.next_action||'Carregando estado operacional...'}</p><strong>Última atualização</strong><p>{state?.updated_at||'sincronizando'}</p><strong>Princípio</strong><p>Uma ação clara, uma evidência real e aprovação humana.</p></div></Card></section></main>}
createRoot(document.getElementById('root')).render(<App/>);
