import { takeUntil } from "rxjs/operators";
import { Component, Input, OnInit } from "@angular/core";
import { NgLifeCycleEvents } from "@synerty/vortexjs";
import { HeaderService } from "@synerty/peek-plugin-base-js";

import {
    PopupLayerSelectionArgsI,
    PrivateDiagramConfigService,
} from "@peek/peek_plugin_diagram/_private/services/PrivateDiagramConfigService";
import { PrivateDiagramLookupService } from "@peek/peek_plugin_diagram/_private/services/PrivateDiagramLookupService";
import { DiagramCoordSetService } from "@peek/peek_plugin_diagram/DiagramCoordSetService";
import { DispLayer } from "@peek/peek_plugin_diagram/_private/lookups";

import { PrivateDiagramCoordSetService } from "@peek/peek_plugin_diagram/_private/services/PrivateDiagramCoordSetService";
import { PeekCanvasConfig } from "../canvas/PeekCanvasConfig.web";
import { PeekCanvasModel } from "../canvas/PeekCanvasModel.web";
import { BehaviorSubject } from "rxjs";
import { BranchDetailTuple } from "@peek/peek_plugin_branch";

@Component({
    selector: "pl-diagram-view-select-layers",
    templateUrl: "select-layers.component.web.html",
    styleUrls: ["select-layers.component.web.scss"],
})
export class SelectLayersComponent extends NgLifeCycleEvents implements OnInit {
    popupShown: boolean = false;

    @Input("coordSetKey")
    coordSetKey: string;

    @Input("modelSetKey")
    modelSetKey: string;

    @Input("model")
    model: PeekCanvasModel;

    @Input("config")
    config: PeekCanvasConfig;

    allItems: DispLayer[] = [];

    items$ = new BehaviorSubject<DispLayer[]>([]);

    private coordSetService: PrivateDiagramCoordSetService;

    private _filterText: string = "";

    constructor(
        private headerService: HeaderService,
        private lookupService: PrivateDiagramLookupService,
        private configService: PrivateDiagramConfigService,
        abstractCoordSetService: DiagramCoordSetService,
    ) {
        super();

        this.coordSetService = <PrivateDiagramCoordSetService>(
            abstractCoordSetService
        );

        this.configService
            .popupLayerSelectionObservable()
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((v: PopupLayerSelectionArgsI) => this.openPopup(v));
    }

    override ngOnInit() {}

    closePopup(): void {
        this.popupShown = false;
        this.allItems = [];
        this.refilter();
    }

    noItems(): boolean {
        return this.items.length == 0;
    }

    get items(): DispLayer[] {
        return this.items$.value;
    }

    get filterText(): string {
        return this._filterText;
    }

    set filterText(value: string) {
        this._filterText = value.toLowerCase();
        this.refilter();
    }

    private refilter(): void {
        const filtByStr = (i) => {
            return (
                this._filterText.length === 0 ||
                i.name.toLowerCase().indexOf(this._filterText) !== -1
            );
        };

        let items = this.allItems.filter((i) => filtByStr(i));

        const compStr = (a, b) => (a == b ? 0 : a < b ? -1 : 1);
        items = items.sort((a, b) =>
            compStr(a.name.toLowerCase(), b.name.toLowerCase()),
        );

        this.items$.next(items);
    }

    toggleLayerVisible(layer: DispLayer): void {
        layer.visible = !layer.visible;
        if (this.model != null) this.model.recompileModel();
    }

    protected openPopup({ coordSetKey, modelSetKey }) {
        let coordSet = this.coordSetService.coordSetForKey(
            modelSetKey,
            coordSetKey,
        );
        console.log("Opening Layer Select popup");

        this.allItems = this.lookupService.layersOrderedByOrder(
            coordSet.modelSetId,
        );
        this.refilter();

        this.popupShown = true;
    }
}
