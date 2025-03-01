# 📊 Painel Estratégico de Crescimento - Cury Company  

## 1. Problema de Negócio  
A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas.  

Através desse aplicativo, é possível realizar o pedido de uma refeição em qualquer restaurante cadastrado e recebê-lo no conforto de casa por um entregador também cadastrado.  

Apesar do crescimento das entregas, o CEO não tem visibilidade completa dos KPIs estratégicos da empresa.  

🎯 Fui contratado como Cientista de Dados para desenvolver soluções que organizem os principais KPIs em uma única ferramenta, permitindo que o CEO tome decisões estratégicas com mais facilidade.

A Cury Company opera no modelo de negócio **Marketplace**, intermediando negócios entre:  
- **Restaurantes**  
- **Entregadores**  
- **Clientes finais**  

### Métricas desejadas pelo CEO  

#### 📌 Do lado da empresa:  
- Quantidade de pedidos por dia e por semana.  
- Distribuição dos pedidos por tipo de tráfego.  
- Comparação do volume de pedidos por cidade e tipo de tráfego.  
- Quantidade de pedidos por entregador por semana.  
- Localização central de cada cidade por tipo de tráfego.  

#### 📌 Do lado do entregador:  
- Idade mínima e máxima dos entregadores.  
- Melhor e pior condição dos veículos.  
- Avaliação média dos entregadores.  
- Avaliação média e desvio padrão por tipo de tráfego e condições climáticas.  
- Top 10 entregadores mais rápidos e mais lentos por cidade.  

#### 📌 Do lado dos restaurantes:  
- Quantidade de entregadores únicos.  
- Distância média dos restaurantes até os locais de entrega.  
- Tempo médio e desvio padrão de entrega por cidade.  
- Tempo médio de entrega por cidade e tipo de pedido.  
- Tempo médio de entrega durante festivais.  

---

## 2. Premissas Assumidas para a Análise  
- A análise foi realizada com dados entre **11/02/2022 e 06/04/2022**.  
- **Marketplace** foi o modelo de negócio assumido.  
- As três principais visões do negócio foram:  
  1. **Visão de transação de pedidos**  
  2. **Visão de restaurantes**  
  3. **Visão de entregadores**  

---

## 3. Estratégia da Solução  

O painel estratégico foi desenvolvido utilizando métricas que refletem as **3 principais visões** do modelo de negócio da empresa:  

### 🔹 Visão do crescimento da empresa  
- Pedidos por dia e por semana.  
- Porcentagem de pedidos por condições de trânsito.  
- Quantidade de pedidos por tipo e por cidade.  
- Quantidade de pedidos por tipo de entrega.  

### 🔹 Visão do crescimento dos restaurantes  
- Quantidade de pedidos únicos.  
- Distância média percorrida.  
- Tempo médio e desvio padrão de entrega durante festivais e dias normais.  
- Tempo médio de entrega por cidade e por tipo de pedido.  

### 🔹 Visão do crescimento dos entregadores  
- Idade do entregador mais velho e do mais novo.  
- Avaliação média por entregador, veículo, tipo de trânsito e clima.  
- Tempo médio dos entregadores mais rápidos por cidade.  

---

## 4. Top 3 Insights de Dados  

1️⃣ A sazonalidade da quantidade de pedidos é diária, com uma variação de aproximadamente **10% em dias consecutivos**.  
2️⃣ Cidades do tipo **Semi-Urban** não possuem condições de trânsito consideradas baixas.  
3️⃣ **As maiores variações no tempo de entrega acontecem durante o clima ensolarado**.  

---

## 5. Produto Final do Projeto  

📌 **Painel online**, hospedado em nuvem e acessível de qualquer dispositivo conectado à internet.  

🔗 **Acesse o painel aqui**: [Project Cury Company](https://thprojects-curry-company-ftc.streamlit.app/)  

---

## 6. Conclusão  

O projeto atingiu seu objetivo de organizar os KPIs estratégicos da empresa.  

🔹 **Conclusão da visão da empresa:** O número de pedidos cresceu entre a **semana 06 e a semana 13 de 2022**.  

---

## 7. Próximos Passos  

✅ **Reduzir o número de métricas** para simplificação.  
✅ **Criar novos filtros** para uma análise mais personalizada.  
✅ **Adicionar novas visões de negócio** para expandir a análise.  
