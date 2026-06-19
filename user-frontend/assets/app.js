function getBoundSource() {
  return {
    ...window.DaeMockData,
    summary: window.DaeDataStore?.summary,
    currentUser: window.DaeDataStore?.summary?.currentUser,
    admin: window.DaeDataStore?.summary?.admin,
  };
}

function getValueByPath(source, path) {
  return path.split(".").reduce((acc, key) => acc?.[key], source);
}

function bindData() {
  const source = getBoundSource();
  document.querySelectorAll("[data-bind]").forEach((el) => {
    const value = getValueByPath(source, el.dataset.bind);
    if (value === undefined) return;

    if ("bindCountup" in el.dataset) {
      el.dataset.countup = value;
      if (!el.textContent.trim()) el.textContent = value;
      return;
    }

    const prefix = el.dataset.prefix || "";
    const suffix = el.dataset.suffix || "";
    el.textContent = `${prefix}${value}${suffix}`;
  });
}

function bindRuntimeStatus() {
  const runtime = window.DaeRuntime || { apiEnabled: false, apiBaseUrl: "-" };

  document.querySelectorAll("[data-runtime-status]").forEach((el) => {
    el.textContent = runtime.apiEnabled ? "本地 API 已连接" : "当前使用演示数据";
    el.classList.toggle("up", !!runtime.apiEnabled);
    el.classList.toggle("down", !runtime.apiEnabled);
  });

  document.querySelectorAll("[data-runtime-base]").forEach((el) => {
    el.textContent = runtime.apiBaseUrl || "-";
  });
}

function animateCount(el) {
  const target = Number(el.dataset.countup || 0);
  const prefix = el.dataset.prefix || "";
  const suffix = el.dataset.suffix || "";
  const duration = 800;
  const start = performance.now();

  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const value = Math.round(target * progress);
    el.textContent = `${prefix}${value}${suffix}`;
    if (progress < 1) requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}

function bindTableFilter(root) {
  const input = root.querySelector("[data-table-search]");
  const selects = Array.from(root.querySelectorAll("[data-table-filter]"));
  const rows = Array.from(root.querySelectorAll("tbody tr[data-row]"));
  const empty = root.querySelector("[data-empty]");

  const apply = () => {
    const keyword = (input?.value || "").trim().toLowerCase();
    let visible = 0;

    rows.forEach((row) => {
      const text = (row.dataset.search || row.textContent).toLowerCase();
      const searchOk = !keyword || text.includes(keyword);
      const filterOk = selects.every((select) => {
        const key = select.dataset.tableFilter;
        const value = select.value;
        return value === "all" || row.dataset[key] === value;
      });
      const show = searchOk && filterOk;
      row.style.display = show ? "" : "none";
      if (show) visible += 1;
    });

    if (empty) {
      empty.style.display = visible ? "none" : "table-row";
    }
  };

  input?.addEventListener("input", apply);
  selects.forEach((select) => select.addEventListener("change", apply));
  apply();
}

function renderProductsRow(item, store) {
  const statusMap = {
    normal: '<span class="tag good">正常销售</span>',
    low: '<span class="tag warn">库存偏低</span>',
    weak: '<span class="tag">动销偏弱</span>',
  };
  const adviceMap = {
    normal: "保持价格，补评价素材",
    low: "建议 3 天内补货",
    weak: "优化主图后再投流",
  };
  const storeName = store.entities.stores.find((row) => row.id === item.storeId)?.name || "-";
  return `
    <tr data-row data-store="${item.storeId}" data-status="${item.status}" data-search="${item.name} ${item.id} ${adviceMap[item.status] || ""}">
      <td><strong>${item.name}</strong><br><span style="color:#6d768c;">SKU: ${item.id}</span></td>
      <td>${storeName}</td>
      <td>¥${item.price || "-"}</td>
      <td>${item.stock}</td>
      <td>${item.weeklyOrders}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${adviceMap[item.status] || "继续观察"}</td>
    </tr>
  `;
}

function renderOrdersRow(item, store) {
  const statusMap = {
    pending: '<span class="tag warn">待发货</span>',
    prepare: '<span class="tag">待备货</span>',
    shipping: '<span class="tag good">运输中</span>',
  };
  const adviceMap = {
    pending: "优先出库",
    prepare: "同步库存",
    shipping: "跟踪签收",
  };
  const storeName = store.entities.stores.find((row) => row.id === item.storeId)?.name || "-";
  const productName = store.entities.products.find((row) => row.id === item.productId)?.name || "-";
  return `
    <tr data-row data-status="${item.status}" data-store="${item.storeId}" data-search="${item.id} ${productName} ${adviceMap[item.status] || ""}">
      <td><strong>${item.id}</strong></td>
      <td>${productName}</td>
      <td>${storeName}</td>
      <td>¥${item.amount}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.time || "-"}</td>
      <td>${adviceMap[item.status] || "继续跟进"}</td>
    </tr>
  `;
}

function renderStoresRow(item, store) {
  const authMap = {
    api: '<span class="tag good">Seller API</span>',
    cookie: '<span class="tag warn">Cookie</span>',
  };
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    error: '<span class="tag bad">异常</span>',
  };
  const advice = item.status === "error" ? "重新授权" : item.auth === "cookie" ? "建议迁移 API" : "继续使用";
  return `
    <tr data-row data-auth="${item.auth}" data-status="${item.status}" data-search="${item.name} ${item.site} ${advice}">
      <td><strong>${item.name}</strong></td>
      <td>${item.site}</td>
      <td>${authMap[item.auth] || '<span class="tag">未知</span>'}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.syncedAt || "-"}</td>
      <td class="${item.health >= 80 ? "up" : item.health >= 60 ? "mid" : "down"}">${item.health}</td>
      <td>${advice}</td>
    </tr>
  `;
}

function renderCampaignsRow(item, store) {
  const statusMap = {
    running: '<span class="tag good">进行中</span>',
    applying: '<span class="tag warn">报名中</span>',
    review: '<span class="tag">待复盘</span>',
    pending: '<span class="tag warn">待报名</span>',
  };
  const adviceMap = {
    running: "继续推主力款",
    applying: "补足素材",
    review: "分析转化变化",
    pending: "确认价格带",
  };
  const storeName = store.entities.stores.find((row) => row.id === item.storeId)?.name || "-";
  return `
    <tr data-row data-store="${item.storeId}" data-status="${item.status}" data-search="${item.name} ${storeName} ${adviceMap[item.status] || ""}">
      <td><strong>${item.name}</strong></td>
      <td>${storeName}</td>
      <td>${item.dateRange || "待定"}</td>
      <td>${item.items}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${adviceMap[item.status] || "继续观察"}</td>
    </tr>
  `;
}

function renderSuppliersRow(item) {
  const categoryMap = {
    pet: "宠物清洁",
    home: "家居收纳",
    outdoor: "户外露营",
    beauty: "美妆收纳",
  };
  const gradeMap = {
    a: '<span class="tag good">A</span>',
    bplus: '<span class="tag warn">B+</span>',
    b: '<span class="tag">B</span>',
  };
  const note = item.core ? "支持长期合作" : item.quotePending ? "待更新报价" : item.sampling ? "样品跟进中" : "可持续观察";
  return `
    <tr data-row data-category="${item.category}" data-grade="${item.grade}" data-search="${item.name} ${categoryMap[item.category] || ""} ${note}">
      <td><strong>${item.name}</strong></td>
      <td>${categoryMap[item.category] || "-"}</td>
      <td>${item.moq || "-"}</td>
      <td>${item.quote || "-"}</td>
      <td>${item.leadTime || "-"}</td>
      <td>${gradeMap[item.grade] || '<span class="tag">-</span>'}</td>
      <td>${note}</td>
    </tr>
  `;
}

function renderUsersRow(item) {
  const statusMap = {
    active: '<span class="tag good">正常</span>',
    pending: '<span class="tag">待配置</span>',
    disabled: '<span class="tag bad">已停用</span>',
  };
  const planMap = {
    free_analysis: '<span class="tag good">免费分析</span>',
    setup_pending: '<span class="tag warn">待完善授权</span>',
  };
  return `
    <tr data-row data-plan="${item.plan}" data-status="${item.status}" data-search="${item.name} ${item.email} ${item.focus}">
      <td><strong>${item.name}</strong><br><span style="color:#6d768c;">${item.email}</span></td>
      <td>${item.registeredAt}</td>
      <td>${item.storesBound}</td>
      <td>${planMap[item.plan] || '<span class="tag">未设置</span>'}</td>
      <td>${item.lastActive}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
    </tr>
  `;
}

function renderAdminStoresRow(item, store) {
  const owner = store.entities.users.find((row) => row.id === item.ownerId);
  const authMap = {
    api: '<span class="tag good">Seller API</span>',
    cookie: '<span class="tag warn">Cookie</span>',
  };
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    error: '<span class="tag bad">异常</span>',
  };
  return `
    <tr data-row data-auth="${item.auth}" data-status="${item.status}" data-search="${owner?.name || ""} ${item.name} ${item.note || ""}">
      <td>${owner?.name || "-"}</td>
      <td>${item.name}</td>
      <td>${authMap[item.auth] || '<span class="tag">未知</span>'}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.syncedAt || "-"}</td>
      <td>${item.note || "-"}</td>
    </tr>
  `;
}

function renderCurrentStoresRow(item) {
  const authMap = {
    api: '<span class="tag good">Seller API</span>',
    cookie: '<span class="tag warn">Cookie</span>',
  };
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    error: '<span class="tag bad">异常</span>',
  };
  return `
    <tr data-row data-auth="${item.auth}" data-status="${item.status}" data-search="${item.name} ${item.site} ${item.note || ""}">
      <td><strong>${item.name}</strong></td>
      <td>${item.site}</td>
      <td>${authMap[item.auth] || '<span class="tag">未知</span>'}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.syncedAt || "-"}</td>
      <td>${item.note || "-"}</td>
    </tr>
  `;
}

function renderSyncJobsRow(item) {
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    running: '<span class="tag good">运行中</span>',
    warn: '<span class="tag warn">待优化</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.name} ${item.source} ${item.frequency}">
      <td>${item.name}</td>
      <td>${item.source}</td>
      <td>${item.frequency}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.lastRun}</td>
    </tr>
  `;
}

function renderSelectionCategoriesRow(item) {
  return `
    <tr data-row data-search="${item.name} ${item.note} ${item.trend}">
      <td><strong>${item.name}</strong></td>
      <td>${item.demand}</td>
      <td>${item.competition}</td>
      <td>${item.margin}</td>
      <td>${item.trend}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderSelectionKeywordsRow(item) {
  return `
    <tr data-row data-search="${item.keyword} ${item.category} ${item.action}">
      <td><strong>${item.keyword}</strong></td>
      <td>${item.category}</td>
      <td>${item.heat}</td>
      <td>${item.difficulty}</td>
      <td>${item.action}</td>
    </tr>
  `;
}

function renderSelectionProductsRow(item) {
  return `
    <tr data-row data-search="${item.name} ${item.category} ${item.source}">
      <td><strong>${item.name}</strong></td>
      <td>${item.category}</td>
      <td>${item.score}</td>
      <td>${item.margin}</td>
      <td>${item.risk}</td>
      <td>${item.source}</td>
    </tr>
  `;
}

function renderDraftProductsRow(item) {
  const statusMap = {
    image: '<span class="tag warn">待补图</span>',
    attribute: '<span class="tag">待补属性</span>',
    pricing: '<span class="tag warn">待定价</span>',
    ready: '<span class="tag good">待发布</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.name} ${item.source} ${item.nextStep}">
      <td><strong>${item.name}</strong></td>
      <td>${item.source}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.missing}</td>
      <td>${item.suggestedPrice}</td>
      <td>${item.nextStep}</td>
    </tr>
  `;
}

function renderInventoryAlertsRow(item) {
  const statusMap = {
    urgent: '<span class="tag warn">紧急补货</span>',
    warn: '<span class="tag warn">建议补货</span>',
    healthy: '<span class="tag good">库存健康</span>',
    hold: '<span class="tag">暂不补货</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.name} ${item.status} ${item.restock}">
      <td><strong>${item.name}</strong></td>
      <td>${item.available}</td>
      <td>${item.sales7d}</td>
      <td>${item.days}</td>
      <td>${item.inTransit}</td>
      <td>${item.restock}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
    </tr>
  `;
}

function renderSamplesRow(item, store) {
  const supplierName = store.entities.suppliers.find((row) => row.id === item.supplierId)?.name || "-";
  const statusMap = {
    arrived: '<span class="tag good">已到样</span>',
    review: '<span class="tag warn">待评估</span>',
    shipping: '<span class="tag">在途</span>',
    pending: '<span class="tag warn">待寄样</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.name} ${supplierName} ${item.nextStep}">
      <td><strong>${item.name}</strong></td>
      <td>${supplierName}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.arrival}</td>
      <td>${item.result}</td>
      <td>${item.nextStep}</td>
    </tr>
  `;
}

function renderPurchasesRow(item, store) {
  const supplierName = store.entities.suppliers.find((row) => row.id === item.supplierId)?.name || "-";
  const statusMap = {
    pending: '<span class="tag warn">待下单</span>',
    production: '<span class="tag good">生产中</span>',
    shipping: '<span class="tag">在途</span>',
    risk: '<span class="tag warn">逾期风险</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.id} ${item.product} ${supplierName} ${item.note}">
      <td><strong>${item.id}</strong></td>
      <td>${item.product}</td>
      <td>${supplierName}</td>
      <td>${item.quantity}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.eta}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderToolRatesRow(item) {
  return `
    <tr data-row data-search="${item.cnyCost} ${item.rubPrice} ${item.note}">
      <td>${item.cnyCost}</td>
      <td>${item.rubPrice}</td>
      <td>${item.margin}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderToolTaxesRow(item) {
  return `
    <tr data-row data-search="${item.item} ${item.note}">
      <td><strong>${item.item}</strong></td>
      <td>${item.value}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderToolTemplatesRow(item) {
  return `
    <tr data-row data-search="${item.type} ${item.category} ${item.content}">
      <td><strong>${item.type}</strong></td>
      <td>${item.category}</td>
      <td>${item.content}</td>
    </tr>
  `;
}

function renderStoreConfigsRow(item, store) {
  const storeName = store.entities.stores.find((row) => row.id === item.storeId)?.name || "-";
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    warn: '<span class="tag warn">待优化</span>',
    error: '<span class="tag bad">异常</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-store="${item.storeId}" data-search="${storeName} ${item.configItem} ${item.note}">
      <td><strong>${storeName}</strong></td>
      <td>${item.configItem}</td>
      <td>${item.channel}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.updatedAt}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderAnalysisProductsRow(item) {
  const riskMap = {
    healthy: '<span class="tag good">健康</span>',
    warn: '<span class="tag warn">库存紧张</span>',
    low: '<span class="tag">转化偏低</span>',
  };
  return `
    <tr data-row data-risk="${item.risk}" data-search="${item.name} ${item.advice}">
      <td><strong>${item.name}</strong></td>
      <td>${item.impressions}</td>
      <td>${item.ctr}</td>
      <td>${item.conversion}</td>
      <td>${item.sales7d}</td>
      <td>${riskMap[item.risk] || '<span class="tag">未知</span>'}</td>
      <td>${item.advice}</td>
    </tr>
  `;
}

function renderAnalysisOrdersRow(item) {
  const trendClass =
    item.trend.includes("稳定") || item.trend.includes("下降")
      ? "up"
      : item.trend.includes("处理")
        ? "down"
        : "mid";
  return `
    <tr data-row data-search="${item.dimension} ${item.trend} ${item.advice}">
      <td><strong>${item.dimension}</strong></td>
      <td>${item.quantity}</td>
      <td>${item.ratio}</td>
      <td class="${trendClass}">${item.trend}</td>
      <td>${item.advice}</td>
    </tr>
  `;
}

function renderAdminServicesRow(item) {
  const statusMap = {
    normal: '<span class="tag good">正常</span>',
    running: '<span class="tag good">运行中</span>',
    warn: '<span class="tag warn">待优化</span>',
  };
  return `
    <tr data-row data-status="${item.status}" data-search="${item.name} ${item.scope} ${item.note}">
      <td><strong>${item.name}</strong></td>
      <td>${item.scope}</td>
      <td>${item.access}</td>
      <td>${statusMap[item.status] || '<span class="tag">未知</span>'}</td>
      <td>${item.owner}</td>
      <td>${item.note}</td>
    </tr>
  `;
}

function renderTableRows() {
  const store = window.DaeDataStore;
  if (!store?.entities) return;

  document.querySelectorAll("[data-render-source]").forEach((tbody) => {
    const list = getValueByPath(store, tbody.dataset.renderSource);
    if (!Array.isArray(list)) return;

    const type = tbody.dataset.renderType;
    const rows = list.map((item) => {
      if (type === "products") return renderProductsRow(item, store);
      if (type === "orders") return renderOrdersRow(item, store);
      if (type === "stores") return renderStoresRow(item, store);
      if (type === "campaigns") return renderCampaignsRow(item, store);
      if (type === "suppliers") return renderSuppliersRow(item);
      if (type === "users") return renderUsersRow(item);
      if (type === "admin-stores") return renderAdminStoresRow(item, store);
      if (type === "current-stores") return renderCurrentStoresRow(item);
      if (type === "sync-jobs") return renderSyncJobsRow(item);
      if (type === "selection-categories") return renderSelectionCategoriesRow(item);
      if (type === "selection-keywords") return renderSelectionKeywordsRow(item);
      if (type === "selection-products") return renderSelectionProductsRow(item);
      if (type === "draft-products") return renderDraftProductsRow(item);
      if (type === "inventory-alerts") return renderInventoryAlertsRow(item);
      if (type === "samples") return renderSamplesRow(item, store);
      if (type === "purchases") return renderPurchasesRow(item, store);
      if (type === "tool-rates") return renderToolRatesRow(item);
      if (type === "tool-taxes") return renderToolTaxesRow(item);
      if (type === "tool-templates") return renderToolTemplatesRow(item);
      if (type === "store-configs") return renderStoreConfigsRow(item, store);
      if (type === "analysis-products") return renderAnalysisProductsRow(item);
      if (type === "analysis-orders") return renderAnalysisOrdersRow(item);
      if (type === "admin-services") return renderAdminServicesRow(item);
      return "";
    }).join("");

    tbody.innerHTML = `${rows}<tr data-empty style="display:none;"><td colspan="${tbody.dataset.emptyCols || 7}" class="empty-state">没有匹配的结果，换个关键词或筛选条件试试。</td></tr>`;
  });
}

async function startApp() {
  if (!window.DaeApi) {
    const appScript = Array.from(document.scripts).find((script) =>
      /assets\/app\.js$/.test(script.getAttribute("src") || "")
    );

    if (appScript) {
      await new Promise((resolve) => {
        const apiScript = document.createElement("script");
        apiScript.src = appScript.src.replace(/app\.js$/, "api.js");
        apiScript.onload = () => resolve();
        apiScript.onerror = () => resolve();
        document.head.appendChild(apiScript);
      });
    }
  }

  if (window.DaeApi?.bootstrapDashboardData) {
    await window.DaeApi.bootstrapDashboardData();
  }

  bindData();
  bindRuntimeStatus();
  renderTableRows();
  document.querySelectorAll("[data-countup], [data-bind-countup]").forEach(animateCount);
  document.querySelectorAll("[data-table-root]").forEach(bindTableFilter);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", startApp, { once: true });
} else {
  startApp();
}
