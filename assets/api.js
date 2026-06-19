(function () {
  const API_BASE_KEY = "dae_api_base_url";
  const TOKEN_KEY = "dae_access_token";
  const USER_ID_KEY = "dae_user_id";
  const DEFAULT_BASE_URL = "";

  function getBaseUrl() {
    const configuredBase =
      window.DAE_API_BASE_URL !== undefined
        ? window.DAE_API_BASE_URL
        : window.__DAE_API_BASE_URL__ !== undefined
          ? window.__DAE_API_BASE_URL__
          : window.localStorage.getItem(API_BASE_KEY) || DEFAULT_BASE_URL;
    return String(configuredBase || "").replace(/\/$/, "");
  }

  function setBaseUrl(url) {
    const value = (url || "").trim().replace(/\/$/, "");
    if (value) {
      window.localStorage.setItem(API_BASE_KEY, value);
    }
  }

  function getUserId() {
    return window.localStorage.getItem(USER_ID_KEY) || "";
  }

  function setSession(token, userId) {
    if (token) window.localStorage.setItem(TOKEN_KEY, token);
    if (userId) window.localStorage.setItem(USER_ID_KEY, userId);
  }

  function clearSession() {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_ID_KEY);
  }

  async function request(path, options) {
    const response = await fetch(`${getBaseUrl()}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    });

    const isJson = response.headers.get("content-type")?.includes("application/json");
    const payload = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      const detail =
        typeof payload === "object" && payload !== null
          ? payload.detail || payload.message || "请求失败"
          : payload || "请求失败";
      throw new Error(detail);
    }

    return payload;
  }

  function mapStore(item) {
    return {
      id: item.id,
      ownerId: item.owner_id,
      name: item.name,
      site: item.site,
      auth: item.auth,
      status: item.status,
      health: item.health,
      syncedAt: item.synced_at,
      note: item.note,
    };
  }

  function mapToolRate(item) {
    return {
      id: item.id,
      cnyCost: item.cny_cost,
      rubPrice: item.rub_price,
      margin: item.margin,
      note: item.note,
    };
  }

  function mapAdminJob(item) {
    return {
      id: item.id,
      name: item.name,
      source: item.source,
      frequency: item.frequency,
      status: item.status,
      lastRun: item.last_run,
    };
  }

  function mapProduct(item) {
    return {
      id: item.id,
      name: item.name,
      storeId: item.store_id,
      stock: item.stock,
      weeklyOrders: item.weekly_orders,
      status: item.status,
      price: item.price,
    };
  }

  function mapDraft(item) {
    return {
      id: item.id,
      name: item.name,
      source: item.source,
      status: item.status,
      missing: item.missing,
      suggestedPrice: item.suggested_price,
      nextStep: item.next_step,
    };
  }

  function mapInventory(item) {
    return {
      id: item.id,
      name: item.name,
      available: item.available,
      sales7d: item.sales_7d,
      days: item.days,
      inTransit: item.in_transit,
      restock: item.restock,
      status: item.status,
    };
  }

  function mergeDashboardData(result) {
    if (!window.DaeDataStore) return;

    const store = window.DaeDataStore;
    const currentUserId = getUserId() || store.currentUserId;

    if (result.me) {
      store.summary.currentUser = {
        ...store.summary.currentUser,
        name: result.me.name,
        email: result.me.email,
        planLabel: result.me.plan_label,
        storesBound: result.me.stores_bound,
        analysisAccess: result.me.analysis_access,
        nextStep: result.me.next_step,
        roleLabel: result.me.role_label,
        verifiedLabel: result.me.verified_label,
        focus: result.me.focus,
      };
    }

    if (Array.isArray(result.stores)) {
      const stores = result.stores.map(mapStore);
      store.entities.stores = stores;
      store.entities.currentUserStores = stores.filter((item) => item.ownerId === currentUserId);
      store.summary.stores = {
        ...store.summary.stores,
        total: stores.length,
        api: stores.filter((item) => item.auth === "api").length,
        cookie: stores.filter((item) => item.auth === "cookie").length,
        error: stores.filter((item) => item.status === "error").length,
        avgHealth: stores.length
          ? Math.round(stores.reduce((sum, item) => sum + item.health, 0) / stores.length)
          : 0,
      };
    }

    if (Array.isArray(result.storeConfigs)) {
      store.entities.storeConfigs = result.storeConfigs.map((item) => ({
        id: item.id,
        storeId: item.store_id,
        configItem: item.config_item,
        channel: item.channel,
        status: item.status,
        updatedAt: item.updated_at,
        note: item.note,
      }));
    }

    if (result.productsOverview) {
      store.summary.products = {
        ...store.summary.products,
        online: result.productsOverview.online,
        lowStock: result.productsOverview.low_stock,
        active: result.productsOverview.active,
        optimize: result.productsOverview.optimize,
        drafts: result.productsOverview.drafts,
        draftsImages: result.productsOverview.drafts_images,
        draftsPricing: result.productsOverview.drafts_pricing,
        readyToPublish: result.productsOverview.ready_to_publish,
        alerts: result.productsOverview.alerts,
        inTransit: result.productsOverview.in_transit,
        turnoverDays: result.productsOverview.turnover_days,
        restockPlans: result.productsOverview.restock_plans,
      };
    }

    if (Array.isArray(result.productsOnline)) {
      store.entities.products = result.productsOnline.map(mapProduct);
    }

    if (Array.isArray(result.productDrafts)) {
      store.entities.draftProducts = result.productDrafts.map(mapDraft);
    }

    if (Array.isArray(result.inventoryAlerts)) {
      store.entities.inventoryAlerts = result.inventoryAlerts.map(mapInventory);
    }

    if (Array.isArray(result.users)) {
      store.entities.users = result.users.map((item) => ({
        id: item.id,
        name: item.name,
        email: item.email,
        phone: item.phone,
        registeredAt: item.registered_at,
        storesBound: item.stores_bound,
        plan: item.plan,
        planLabel: item.plan_label,
        lastActive: item.last_active,
        status: item.status,
        roleLabel: item.role_label,
        focus: item.focus,
        verified: item.verified,
        nextStep: item.next_step,
      }));
      store.summary.users = {
        total: store.entities.users.length,
        recent: store.entities.users.filter((item) => item.registeredAt >= "2026-06-15").length,
        free: store.entities.users.filter((item) => item.plan === "free_analysis").length,
        bound: store.entities.users.filter((item) => item.storesBound > 0).length,
      };
    }

    if (Array.isArray(result.selectionCategories)) {
      store.entities.selectionCategories = result.selectionCategories;
    }

    if (Array.isArray(result.selectionKeywords)) {
      store.entities.selectionKeywords = result.selectionKeywords;
    }

    if (Array.isArray(result.selectionProducts)) {
      store.entities.selectionProducts = result.selectionProducts;
    }

    if (result.selectionOverview) {
      store.summary.selection = {
        ...store.summary.selection,
        hotCategories: result.selectionOverview.hot_categories,
        trackedKeywords: result.selectionOverview.tracked_keywords,
        candidateProducts: result.selectionOverview.candidate_products,
        opportunities: result.selectionOverview.opportunities,
      };
    }

    if (result.analysisOverview) {
      store.summary.analysis = {
        ...store.summary.analysis,
        freePages: result.analysisOverview.free_pages,
        salesToday: result.analysisOverview.sales_today,
      };
      store.summary.orders = {
        ...store.summary.orders,
        today: result.analysisOverview.orders_today,
        pending: result.analysisOverview.pending_orders,
      };
      store.summary.stores = {
        ...store.summary.stores,
        avgHealth: result.analysisOverview.avg_health,
      };
    }

    if (Array.isArray(result.analysisProducts)) {
      store.entities.analysisProducts = result.analysisProducts.map((item) => ({
        id: item.id,
        name: item.name,
        impressions: item.impressions,
        ctr: item.ctr,
        conversion: item.conversion,
        sales7d: item.sales_7d,
        risk: item.risk,
        advice: item.advice,
      }));
    }

    if (Array.isArray(result.analysisOrders)) {
      store.entities.analysisOrders = result.analysisOrders.map((item) => ({
        id: item.id,
        dimension: item.dimension,
        quantity: item.quantity,
        ratio: item.ratio,
        trend: item.trend,
        advice: item.advice,
      }));
    }

    if (Array.isArray(result.toolRates)) {
      store.entities.toolRates = result.toolRates.map(mapToolRate);
    }

    if (Array.isArray(result.toolTaxes)) {
      store.entities.toolTaxes = result.toolTaxes;
    }

    if (Array.isArray(result.toolTemplates)) {
      store.entities.toolTemplates = result.toolTemplates;
    }

    if (result.adminSummary) {
      store.summary.admin = {
        registeredUsers: result.adminSummary.registered_users,
        connectedStores: result.adminSummary.connected_stores,
        activeSyncJobs: result.adminSummary.active_sync_jobs,
        freeAnalysisUsers: result.adminSummary.free_analysis_users,
      };
    }

    if (Array.isArray(result.adminServices)) {
      store.entities.adminServices = result.adminServices.map((item) => ({
        id: item.id,
        name: item.name,
        scope: item.scope,
        access: item.access,
        status: item.status,
        owner: item.owner,
        note: item.note,
      }));
    }

    if (Array.isArray(result.adminJobs)) {
      store.entities.syncJobs = result.adminJobs.map(mapAdminJob);
    }

    window.DaeMockData = store.summary;
  }

  async function bootstrapDashboardData() {
    if (window.DAE_STATIC_DEMO_MODE) {
      window.DaeRuntime = {
        apiEnabled: false,
        apiBaseUrl: getBaseUrl(),
        lastError: "GitHub Pages 静态演示模式，当前使用本地演示数据。",
      };
      return false;
    }

    try {
      const userId = getUserId();
      const [
        me,
        stores,
        storeConfigs,
        users,
        productsOverview,
        productsOnline,
        productDrafts,
        inventoryAlerts,
        selectionOverview,
        analysisOverview,
        analysisProducts,
        analysisOrders,
        selectionCategories,
        selectionKeywords,
        selectionProducts,
        toolRates,
        toolTaxes,
        toolTemplates,
        adminSummary,
        adminServices,
        adminJobs,
      ] = await Promise.all([
        request(`/api/users/me${userId ? `?user_id=${encodeURIComponent(userId)}` : ""}`),
        request("/api/stores"),
        request("/api/stores/configs"),
        request("/api/admin/users"),
        request("/api/products/overview"),
        request("/api/products/online"),
        request("/api/products/drafts"),
        request("/api/products/inventory"),
        request("/api/selection/overview"),
        request("/api/analysis/overview"),
        request("/api/analysis/products"),
        request("/api/analysis/orders"),
        request("/api/selection/categories"),
        request("/api/selection/keywords"),
        request("/api/selection/products"),
        request("/api/tools/rates"),
        request("/api/tools/taxes"),
        request("/api/tools/templates"),
        request("/api/admin/summary"),
        request("/api/admin/services"),
        request("/api/admin/jobs"),
      ]);

      mergeDashboardData({
        me,
        stores,
        users,
        storeConfigs,
        productsOverview,
        productsOnline,
        productDrafts,
        inventoryAlerts,
        selectionOverview,
        analysisOverview,
        analysisProducts,
        analysisOrders,
        selectionCategories,
        selectionKeywords,
        selectionProducts,
        toolRates,
        toolTaxes,
        toolTemplates,
        adminSummary,
        adminServices,
        adminJobs,
      });

      window.DaeRuntime = {
        apiEnabled: true,
        apiBaseUrl: getBaseUrl(),
      };
      return true;
    } catch (error) {
      window.DaeRuntime = {
        apiEnabled: false,
        apiBaseUrl: getBaseUrl(),
        lastError: error.message,
      };
      return false;
    }
  }

  window.DaeApi = {
    getBaseUrl,
    setBaseUrl,
    getUserId,
    setSession,
    clearSession,
    request,
    bootstrapDashboardData,
    login(payload) {
      return request("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    },
    register(payload) {
      return request("/api/auth/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    },
    connectStore(payload) {
      const userId = getUserId();
      const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
      return request(`/api/stores/connect${query}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
    },
  };
})();
