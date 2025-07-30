var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
import { defineComponent, computed, ref, openBlock, createBlock, unref, withCtx, createElementVNode, toDisplayString, createVNode, createElementBlock, createCommentVNode, normalizeClass } from "vue";
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Divider from "primevue/divider";
import Skeleton from "primevue/skeleton";
import TabPanel from "primevue/tabpanel";
import { useI18n } from "vue-i18n";
import { aI as useDialogService, bD as useFirebaseAuthStore, aH as useFirebaseAuthActions, aJ as _sfc_main$1, bE as formatMetronomeCurrency } from "./index-3TQRCtwm.js";
import "@primevue/themes";
import "@primevue/themes/aura";
import "primevue/config";
import "primevue/confirmationservice";
import "primevue/toastservice";
import "primevue/tooltip";
import "primevue/blockui";
import "primevue/progressspinner";
import "@primevue/core";
import "primevue/dialog";
import "primevue/scrollpanel";
import "primevue/message";
import "primevue/usetoast";
import "primevue/card";
import "@primevue/forms";
import "@primevue/forms/resolvers/zod";
import "primevue/checkbox";
import "primevue/dropdown";
import "primevue/inputtext";
import "primevue/panel";
import "primevue/textarea";
import "primevue/listbox";
import "primevue/progressbar";
import "primevue/floatlabel";
import "primevue/tabpanels";
import "primevue/tabs";
import "primevue/iconfield";
import "primevue/inputicon";
import "primevue/badge";
import "primevue/chip";
import "primevue/select";
import "primevue/tag";
import "primevue/inputnumber";
import "primevue/toggleswitch";
import "primevue/colorpicker";
import "primevue/knob";
import "primevue/slider";
import "primevue/password";
import "primevue/popover";
import "primevue/tab";
import "primevue/tablist";
import "primevue/multiselect";
import "primevue/autocomplete";
import "primevue/tabmenu";
import "primevue/dataview";
import "primevue/selectbutton";
import "primevue/contextmenu";
import "primevue/tree";
import "primevue/toolbar";
import "primevue/confirmpopup";
import "primevue/useconfirm";
import "primevue/galleria";
import "primevue/confirmdialog";
const _hoisted_1 = { class: "flex flex-col h-full" };
const _hoisted_2 = { class: "text-2xl font-bold mb-2" };
const _hoisted_3 = { class: "flex flex-col gap-2" };
const _hoisted_4 = { class: "text-sm font-medium text-muted" };
const _hoisted_5 = { class: "flex justify-between items-center" };
const _hoisted_6 = { class: "flex flex-row items-center" };
const _hoisted_7 = {
  key: 1,
  class: "text-xs text-muted"
};
const _hoisted_8 = { class: "flex justify-between items-center mt-8" };
const _hoisted_9 = {
  key: 0,
  class: "flex-grow"
};
const _hoisted_10 = { class: "text-sm font-medium" };
const _hoisted_11 = { class: "text-xs text-muted" };
const _hoisted_12 = { class: "flex flex-row gap-2" };
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "CreditsPanel",
  setup(__props) {
    const { t } = useI18n();
    const dialogService = useDialogService();
    const authStore = useFirebaseAuthStore();
    const authActions = useFirebaseAuthActions();
    const loading = computed(() => authStore.loading);
    const balanceLoading = computed(() => authStore.isFetchingBalance);
    const formattedLastUpdateTime = computed(
      () => authStore.lastBalanceUpdateTime ? authStore.lastBalanceUpdateTime.toLocaleString() : ""
    );
    const handlePurchaseCreditsClick = /* @__PURE__ */ __name(() => {
      dialogService.showTopUpCreditsDialog();
    }, "handlePurchaseCreditsClick");
    const handleCreditsHistoryClick = /* @__PURE__ */ __name(async () => {
      await authActions.accessBillingPortal();
    }, "handleCreditsHistoryClick");
    const handleMessageSupport = /* @__PURE__ */ __name(() => {
      dialogService.showIssueReportDialog({
        title: t("issueReport.contactSupportTitle"),
        subtitle: t("issueReport.contactSupportDescription"),
        panelProps: {
          errorType: "BillingSupport",
          defaultFields: ["Workflow", "Logs", "SystemStats", "Settings"]
        }
      });
    }, "handleMessageSupport");
    const handleFaqClick = /* @__PURE__ */ __name(() => {
      window.open("https://docs.comfy.org/tutorials/api-nodes/faq", "_blank");
    }, "handleFaqClick");
    const creditHistory = ref([]);
    return (_ctx, _cache) => {
      return openBlock(), createBlock(unref(TabPanel), {
        value: "Credits",
        class: "credits-container h-full"
      }, {
        default: withCtx(() => [
          createElementVNode("div", _hoisted_1, [
            createElementVNode("h2", _hoisted_2, toDisplayString(_ctx.$t("credits.credits")), 1),
            createVNode(unref(Divider)),
            createElementVNode("div", _hoisted_3, [
              createElementVNode("h3", _hoisted_4, toDisplayString(_ctx.$t("credits.yourCreditBalance")), 1),
              createElementVNode("div", _hoisted_5, [
                createVNode(_sfc_main$1, { "text-class": "text-3xl font-bold" }),
                loading.value ? (openBlock(), createBlock(unref(Skeleton), {
                  key: 0,
                  width: "2rem",
                  height: "2rem"
                })) : (openBlock(), createBlock(unref(Button), {
                  key: 1,
                  label: _ctx.$t("credits.purchaseCredits"),
                  loading: loading.value,
                  onClick: handlePurchaseCreditsClick
                }, null, 8, ["label", "loading"]))
              ]),
              createElementVNode("div", _hoisted_6, [
                balanceLoading.value ? (openBlock(), createBlock(unref(Skeleton), {
                  key: 0,
                  width: "12rem",
                  height: "1rem",
                  class: "text-xs"
                })) : formattedLastUpdateTime.value ? (openBlock(), createElementBlock("div", _hoisted_7, toDisplayString(_ctx.$t("credits.lastUpdated")) + ": " + toDisplayString(formattedLastUpdateTime.value), 1)) : createCommentVNode("", true),
                createVNode(unref(Button), {
                  icon: "pi pi-refresh",
                  text: "",
                  size: "small",
                  severity: "secondary",
                  onClick: _cache[0] || (_cache[0] = () => unref(authActions).fetchBalance())
                })
              ])
            ]),
            createElementVNode("div", _hoisted_8, [
              createVNode(unref(Button), {
                label: _ctx.$t("credits.invoiceHistory"),
                text: "",
                severity: "secondary",
                icon: "pi pi-arrow-up-right",
                loading: loading.value,
                onClick: handleCreditsHistoryClick
              }, null, 8, ["label", "loading"])
            ]),
            creditHistory.value.length > 0 ? (openBlock(), createElementBlock("div", _hoisted_9, [
              createVNode(unref(DataTable), {
                value: creditHistory.value,
                "show-headers": false
              }, {
                default: withCtx(() => [
                  createVNode(unref(Column), {
                    field: "title",
                    header: _ctx.$t("g.name")
                  }, {
                    body: withCtx(({ data }) => [
                      createElementVNode("div", _hoisted_10, toDisplayString(data.title), 1),
                      createElementVNode("div", _hoisted_11, toDisplayString(data.timestamp), 1)
                    ]),
                    _: 1
                  }, 8, ["header"]),
                  createVNode(unref(Column), {
                    field: "amount",
                    header: _ctx.$t("g.amount")
                  }, {
                    body: withCtx(({ data }) => [
                      createElementVNode("div", {
                        class: normalizeClass([
                          "text-base font-medium text-center",
                          data.isPositive ? "text-sky-500" : "text-red-400"
                        ])
                      }, toDisplayString(data.isPositive ? "+" : "-") + "$" + toDisplayString(unref(formatMetronomeCurrency)(data.amount, "usd")), 3)
                    ]),
                    _: 1
                  }, 8, ["header"])
                ]),
                _: 1
              }, 8, ["value"])
            ])) : createCommentVNode("", true),
            createVNode(unref(Divider)),
            createElementVNode("div", _hoisted_12, [
              createVNode(unref(Button), {
                label: _ctx.$t("credits.faqs"),
                text: "",
                severity: "secondary",
                icon: "pi pi-question-circle",
                onClick: handleFaqClick
              }, null, 8, ["label"]),
              createVNode(unref(Button), {
                label: _ctx.$t("credits.messageSupport"),
                text: "",
                severity: "secondary",
                icon: "pi pi-comments",
                onClick: handleMessageSupport
              }, null, 8, ["label"])
            ])
          ])
        ]),
        _: 1
      });
    };
  }
});
export {
  _sfc_main as default
};
//# sourceMappingURL=CreditsPanel-YBMIYiu0.js.map
