const daeUsers = [
  {
    id: "user_wyb",
    name: "wang yubo",
    email: "wyb461225@163.com",
    phone: "18057445016",
    registeredAt: "2026-06-12",
    storesBound: 3,
    plan: "free_analysis",
    planLabel: "免费分析",
    lastActive: "今天 12:20",
    status: "active",
    roleLabel: "前台用户",
    focus: "Ozon 选品与上品",
    verified: true,
    nextStep: "完善授权",
  },
  {
    id: "user_qiha",
    name: "QIHA 测试店",
    email: "469475300@qq.com",
    phone: "18000000002",
    registeredAt: "2026-06-10",
    storesBound: 1,
    plan: "setup_pending",
    planLabel: "待完善授权",
    lastActive: "今天 10:45",
    status: "pending",
    roleLabel: "待配置用户",
    focus: "店铺授权接入",
    verified: false,
    nextStep: "补全授权参数",
  },
  {
    id: "user_pethome",
    name: "PetHome Demo",
    email: "demo@daeerp.com",
    phone: "18000000003",
    registeredAt: "2026-06-08",
    storesBound: 2,
    plan: "free_analysis",
    planLabel: "免费分析",
    lastActive: "昨天 18:05",
    status: "active",
    roleLabel: "前台用户",
    focus: "宠物家居跨类目",
    verified: true,
    nextStep: "扩展第二店铺",
  },
];

const daeStores = [
  { id: "store_qiha", ownerId: "user_wyb", name: "QIHA-GEILI", site: "Ozon RU", auth: "api", status: "normal", health: 89, syncedAt: "今天 11:40", note: "测试主店铺" },
  { id: "store_pethome", ownerId: "user_pethome", name: "PetHome Lab", site: "Ozon RU", auth: "cookie", status: "normal", health: 74, syncedAt: "今天 10:55", note: "建议迁移 API" },
  { id: "store_kitchen", ownerId: "user_wyb", name: "Kitchen Nova", site: "Ozon KZ", auth: "cookie", status: "error", health: 48, syncedAt: "昨天 19:20", note: "等待重新授权" },
];

const daeProducts = [
  { id: "DE-PET-001", name: "宠物去浮毛梳", storeId: "store_qiha", stock: 64, weeklyOrders: 38, status: "normal", price: 929 },
  { id: "DE-BEAUTY-017", name: "便携化妆收纳包", storeId: "store_qiha", stock: 21, weeklyOrders: 14, status: "low", price: 1190 },
  { id: "DE-KITCHEN-022", name: "厨房旋转调味架", storeId: "store_kitchen", stock: 108, weeklyOrders: 7, status: "weak", price: 1460 },
  { id: "DE-OUTDOOR-009", name: "露营挂灯", storeId: "store_qiha", stock: 9, weeklyOrders: 19, status: "low", price: 1699 },
];

const daeOrders = [
  { id: "OZ-240619-001", productId: "DE-PET-001", storeId: "store_qiha", amount: 929, status: "pending", time: "10:42" },
  { id: "OZ-240619-004", productId: "DE-OUTDOOR-009", storeId: "store_qiha", amount: 1699, status: "shipping", time: "09:15" },
  { id: "OZ-240619-009", productId: "DE-BEAUTY-017", storeId: "store_pethome", amount: 1190, status: "prepare", time: "11:28" },
  { id: "OZ-240619-013", productId: "DE-KITCHEN-022", storeId: "store_qiha", amount: 1460, status: "pending", time: "12:06" },
];

const daeCampaigns = [
  { id: "camp_pet", name: "夏季宠物清洁专场", storeId: "store_qiha", status: "running", items: 12, dateRange: "06-20 至 06-27" },
  { id: "camp_home", name: "家居收纳周", storeId: "store_pethome", status: "applying", items: 8, dateRange: "06-23 至 06-30" },
  { id: "camp_camp", name: "露营装备折扣节", storeId: "store_qiha", status: "review", items: 5, dateRange: "06-15 至 06-19" },
  { id: "camp_beauty", name: "美妆收纳新品试投", storeId: "store_pethome", status: "pending", items: 4, dateRange: "待定" },
];

const daeSuppliers = [
  { id: "sup_pet", name: "义乌某宠物用品厂", category: "pet", grade: "a", core: true, quotePending: false, sampling: false, moq: 200, quote: "¥14.8", leadTime: "7天" },
  { id: "sup_home", name: "台州收纳制品厂", category: "home", grade: "a", core: true, quotePending: false, sampling: false, moq: 300, quote: "¥11.2", leadTime: "10天" },
  { id: "sup_outdoor", name: "深圳户外灯具商", category: "outdoor", grade: "bplus", core: false, quotePending: true, sampling: true, moq: 100, quote: "¥26.0", leadTime: "12天" },
  { id: "sup_beauty", name: "广州美妆包工厂", category: "beauty", grade: "b", core: false, quotePending: true, sampling: true, moq: 500, quote: "¥9.5", leadTime: "8天" },
];

const daeSyncJobs = [
  { id: "job_selection", name: "选品市场聚合", source: "分析服务", frequency: "每日", status: "normal", lastRun: "今天 03:00" },
  { id: "job_orders", name: "订单状态同步", source: "Ozon 授权店铺", frequency: "10 分钟", status: "running", lastRun: "今天 12:10" },
  { id: "job_logistics", name: "物流费用更新", source: "工具服务", frequency: "每日", status: "warn", lastRun: "今天 08:00" },
];

const daeSelectionCategories = [
  { id: "cat_pet", name: "宠物清洁", demand: "高", competition: "中", margin: "34%", trend: "上升", note: "适合继续深挖白牌款" },
  { id: "cat_home", name: "家居收纳", demand: "高", competition: "高", margin: "26%", trend: "稳定", note: "重在差异化组合" },
  { id: "cat_outdoor", name: "户外露营", demand: "中高", competition: "中", margin: "31%", trend: "季节上升", note: "适合节日活动配合" },
  { id: "cat_beauty", name: "美妆收纳", demand: "中", competition: "中高", margin: "22%", trend: "稳定", note: "注重图片与套装打法" },
];

const daeSelectionKeywords = [
  { id: "kw_pet", keyword: "pet grooming brush", category: "宠物清洁", heat: "8.9", difficulty: "中", action: "适合做主推词" },
  { id: "kw_storage", keyword: "storage organizer", category: "家居收纳", heat: "8.2", difficulty: "高", action: "适合做长尾组合" },
  { id: "kw_camping", keyword: "camping lantern", category: "户外露营", heat: "7.8", difficulty: "中", action: "适合配活动推广" },
  { id: "kw_beauty", keyword: "cosmetic bag", category: "美妆收纳", heat: "7.4", difficulty: "中高", action: "适合轻小件试投" },
];

const daeSelectionProducts = [
  { id: "pick_pet", name: "宠物去浮毛梳", category: "宠物清洁", score: 92, margin: "36%", risk: "低", source: "市场热词 + 现有动销" },
  { id: "pick_storage", name: "桌面分层收纳盒", category: "家居收纳", score: 85, margin: "28%", risk: "中", source: "类目需求稳定" },
  { id: "pick_lantern", name: "露营磁吸挂灯", category: "户外露营", score: 88, margin: "33%", risk: "中", source: "季节趋势上升" },
  { id: "pick_bag", name: "便携化妆收纳包", category: "美妆收纳", score: 79, margin: "24%", risk: "中高", source: "适合低成本测款" },
];

const daeDraftProducts = [
  { id: "draft_pet_bath", name: "宠物洗澡按摩刷", source: "选品中心", status: "image", missing: "主图、白底图", suggestedPrice: "₽ 1,129", nextStep: "上传图片后发布" },
  { id: "draft_bag", name: "旅行收纳压缩袋", source: "采集导入", status: "attribute", missing: "材质、规格", suggestedPrice: "₽ 899", nextStep: "补属性并校验类目" },
  { id: "draft_rack", name: "厨房油壶收纳架", source: "人工创建", status: "ready", missing: "无", suggestedPrice: "₽ 1,369", nextStep: "可直接上架" },
  { id: "draft_trash", name: "车载折叠垃圾桶", source: "选品中心", status: "pricing", missing: "价格方案", suggestedPrice: "未生成", nextStep: "进入定价工具" },
];

const daeInventoryAlerts = [
  { id: "inv_lantern", name: "露营挂灯", available: 9, sales7d: 19, days: 3, inTransit: 40, restock: 120, status: "urgent" },
  { id: "inv_beauty", name: "便携化妆收纳包", available: 21, sales7d: 14, days: 10, inTransit: 0, restock: 80, status: "warn" },
  { id: "inv_pet", name: "宠物去浮毛梳", available: 64, sales7d: 38, days: 12, inTransit: 100, restock: 60, status: "healthy" },
  { id: "inv_kitchen", name: "厨房旋转调味架", available: 108, sales7d: 7, days: 42, inTransit: 0, restock: 0, status: "hold" },
];

const daeSamples = [
  { id: "sample_pet", name: "宠物洗澡按摩刷", supplierId: "sup_pet", status: "arrived", arrival: "06-18", result: "材质和手感通过", nextStep: "进入商品草稿" },
  { id: "sample_lamp", name: "露营挂灯升级款", supplierId: "sup_outdoor", status: "review", arrival: "06-19", result: "亮度待测试", nextStep: "48 小时内复测" },
  { id: "sample_bag", name: "旅行收纳压缩袋", supplierId: "sup_home", status: "shipping", arrival: "预计 06-21", result: "未到样", nextStep: "跟踪物流" },
  { id: "sample_bin", name: "车载折叠垃圾桶", supplierId: "sup_beauty", status: "pending", arrival: "未发出", result: "暂无", nextStep: "催寄样" },
];

const daePurchases = [
  { id: "PO-240619-01", product: "宠物去浮毛梳", supplierId: "sup_pet", quantity: 300, status: "production", eta: "06-25", note: "补爆款库存" },
  { id: "PO-240619-04", product: "露营挂灯", supplierId: "sup_outdoor", quantity: 120, status: "pending", eta: "待定", note: "等样品复测" },
  { id: "PO-240618-09", product: "便携化妆收纳包", supplierId: "sup_beauty", quantity: 500, status: "shipping", eta: "06-24", note: "海运转仓" },
  { id: "PO-240617-03", product: "厨房旋转调味架", supplierId: "sup_home", quantity: 260, status: "risk", eta: "06-20", note: "交期需确认" },
];

const daeToolRates = [
  { id: "rate_1", cnyCost: "¥18", rubPrice: "₽929", margin: "25% - 30%", note: "适合轻小件" },
  { id: "rate_2", cnyCost: "¥25", rubPrice: "₽1,269", margin: "25% - 28%", note: "适合中小件" },
  { id: "rate_3", cnyCost: "¥35", rubPrice: "₽1,699", margin: "22% - 26%", note: "适合功能型商品" },
  { id: "rate_4", cnyCost: "¥48", rubPrice: "₽2,290", margin: "20% - 24%", note: "适合高客单商品" },
];

const daeToolTaxes = [
  { id: "tax_purchase", item: "采购成本", value: "¥18 - ¥48", note: "商品本体成本" },
  { id: "tax_logistics", item: "头程物流", value: "¥4 - ¥12", note: "视体积和重量变化" },
  { id: "tax_fee", item: "平台佣金", value: "12% - 18%", note: "按类目不同调整" },
  { id: "tax_buffer", item: "税费缓冲", value: "3% - 8%", note: "作为成本保护带" },
];

const daeToolTemplates = [
  { id: "tpl_title", type: "标题模板", category: "宠物清洁", content: "【核心功能】+【适用对象】+【材质卖点】+【场景词】" },
  { id: "tpl_selling", type: "卖点模板", category: "家居收纳", content: "节省空间 / 承重稳定 / 安装简单 / 多场景适用" },
  { id: "tpl_detail", type: "详情模板", category: "户外露营", content: "痛点开头 + 场景展示 + 参数说明 + 使用方法 + 包装清单" },
  { id: "tpl_local", type: "本土化模板", category: "美妆收纳", content: "突出收纳效率、外观质感和送礼场景，语气更自然" },
];

function repeatCount(base, target) {
  const items = [...base];
  while (items.length < target) {
    const seed = base[items.length % base.length];
    items.push({ ...seed, id: `${seed.id}_${items.length}` });
  }
  return items;
}

const daeAnalysisProducts = [
  { id: "ana_pet", name: "宠物去浮毛梳", impressions: 28400, ctr: "6.7%", conversion: "3.9%", sales7d: 38, risk: "healthy", advice: "可继续加推" },
  { id: "ana_lamp", name: "露营挂灯", impressions: 17200, ctr: "5.9%", conversion: "4.8%", sales7d: 19, risk: "warn", advice: "先补货再扩量" },
  { id: "ana_rack", name: "厨房旋转调味架", impressions: 23100, ctr: "4.2%", conversion: "1.3%", sales7d: 7, risk: "low", advice: "优化主图和价格" },
];

const daeAnalysisOrders = [
  { id: "ao_pending", dimension: "待发货订单", quantity: 23, ratio: "15.7%", trend: "下午集中", advice: "按爆款优先出货" },
  { id: "ao_shipping", dimension: "运输中订单", quantity: 81, ratio: "55.5%", trend: "稳定", advice: "继续跟踪签收率" },
  { id: "ao_cancel", dimension: "取消订单", quantity: 7, ratio: "4.8%", trend: "下降", advice: "维持库存准确率" },
  { id: "ao_exception", dimension: "异常订单", quantity: 4, ratio: "2.7%", trend: "需处理", advice: "排查物流与库存同步" },
];

const daeAdminServices = [
  { id: "svc_selection", name: "选品中心 API", scope: "市场 / 类目 / 关键词 / 候选商品", access: "前台开放", status: "normal", owner: "选品服务", note: "已供前台选品页调用" },
  { id: "svc_analysis", name: "分析中心 API", scope: "店铺概览 / 商品分析 / 订单结构", access: "前台免费", status: "normal", owner: "分析服务", note: "当前免费，后续可分层收费" },
  { id: "svc_tools", name: "工具服务 API", scope: "汇率 / 税费 / 文案模板", access: "前台开放", status: "warn", owner: "工具服务", note: "后续补交互式计算器" },
];

const daeStoreConfigs = [
  { id: "cfg_qiha_api", storeId: "store_qiha", configItem: "Seller API", channel: "Client ID / API Key", status: "normal", updatedAt: "今天 11:42", note: "主店铺 API 可用" },
  { id: "cfg_qiha_cookie", storeId: "store_qiha", configItem: "浏览器 Cookie", channel: "插件兼容链路", status: "warn", updatedAt: "昨天 20:10", note: "建议逐步迁移到 API" },
  { id: "cfg_kitchen_cookie", storeId: "store_kitchen", configItem: "浏览器 Cookie", channel: "旧授权链路", status: "error", updatedAt: "昨天 19:20", note: "等待重新授权" },
];

const expandedSuppliers = repeatCount(daeSuppliers, 28);
const expandedCampaigns = repeatCount(daeCampaigns, 12);

const currentUser = daeUsers[0];
const currentUserStoreIds = daeStores.filter((item) => item.ownerId === currentUser.id).map((item) => item.id);
const currentUserStores = daeStores.filter((item) => currentUserStoreIds.includes(item.id));

const summary = {
  overview: {
    modules: 8,
    pages: 18,
  },
  products: {
    online: 286,
    lowStock: 17,
    active: 142,
    optimize: 29,
    drafts: 54,
    draftsPending: 11,
    draftsImages: 13,
    draftsPricing: 8,
    readyToPublish: 22,
    alerts: 17,
    inTransit: 23,
    turnoverDays: 18,
    restockPlans: 9,
  },
  orders: {
    today: 146,
    pending: 23,
    exceptions: 4,
    shipped: 81,
  },
  stores: {
    total: daeStores.length,
    api: daeStores.filter((item) => item.auth === "api").length,
    cookie: daeStores.filter((item) => item.auth === "cookie").length,
    error: daeStores.filter((item) => item.status === "error").length,
    avgHealth: Math.round(daeStores.reduce((sum, item) => sum + item.health, 0) / daeStores.length),
  },
  campaigns: {
    total: expandedCampaigns.length,
    running: expandedCampaigns.filter((item) => item.status === "running").length,
    pending: expandedCampaigns.filter((item) => item.status === "pending").length,
    review: expandedCampaigns.filter((item) => item.status === "review").length,
  },
  supply: {
    suppliers: expandedSuppliers.length,
    core: 9,
    quotes: 6,
    samples: 4,
    sampleActive: 11,
    sampleArrived: 4,
    samplePassed: 5,
    sampleRetest: 2,
    purchasePending: 7,
    purchaseProduction: 3,
    purchaseShipping: 5,
    purchaseRisk: 1,
  },
  tools: {
    templates: 16,
    calculators: 3,
  },
  analysis: {
    freePages: 3,
    salesToday: 98600,
  },
  selection: {
    opportunities: 24,
    trackedKeywords: 118,
    candidateProducts: 42,
    hotCategories: 4,
  },
  users: {
    total: 128,
    recent: 19,
    free: 92,
    bound: 57,
  },
  currentUser: {
    name: currentUser.name,
    email: currentUser.email,
    planLabel: "免费版",
    storesBound: currentUserStores.length,
    analysisAccess: "已开通",
    nextStep: currentUser.nextStep,
    roleLabel: currentUser.roleLabel,
    verifiedLabel: currentUser.verified ? "已验证" : "待验证",
    focus: currentUser.focus,
  },
  admin: {
    registeredUsers: 128,
    connectedStores: 36,
    activeSyncJobs: 14,
    freeAnalysisUsers: 92,
  },
};

window.DaeDataStore = {
  currentUserId: currentUser.id,
  entities: {
    users: daeUsers,
    stores: daeStores,
    products: daeProducts,
    orders: daeOrders,
    campaigns: expandedCampaigns,
    suppliers: expandedSuppliers,
    syncJobs: daeSyncJobs,
    analysisProducts: daeAnalysisProducts,
    analysisOrders: daeAnalysisOrders,
    adminServices: daeAdminServices,
    storeConfigs: daeStoreConfigs,
    selectionCategories: daeSelectionCategories,
    selectionKeywords: daeSelectionKeywords,
    selectionProducts: daeSelectionProducts,
    draftProducts: daeDraftProducts,
    inventoryAlerts: daeInventoryAlerts,
    samples: daeSamples,
    purchases: daePurchases,
    toolRates: daeToolRates,
    toolTaxes: daeToolTaxes,
    toolTemplates: daeToolTemplates,
    currentUserStores,
  },
  summary,
};

window.DaeMockData = summary;
