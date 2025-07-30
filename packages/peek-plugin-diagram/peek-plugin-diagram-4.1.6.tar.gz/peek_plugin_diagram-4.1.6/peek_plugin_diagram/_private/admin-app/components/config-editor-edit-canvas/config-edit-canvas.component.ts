import { ChangeDetectionStrategy, Component, OnInit } from "@angular/core";
import {
    NgLifeCycleEvents,
    Tuple,
    TupleDataLoaderDelegate,
    TupleSelector,
} from "@synerty/vortexjs";
import { BalloonMsgService } from "@synerty/peek-plugin-base-js";
import { filter, skip, takeUntil } from "rxjs/operators";
import { AbstractControl, FormArray, FormGroup } from "@angular/forms";
import { BehaviorSubject, Subject } from "rxjs";
import { DiagramTupleService } from "../../services/diagram-tuple-service";
import { DiagramConfigStateService } from "../../services/diagram-config-state-service";
import { ConfigCanvasDataLoaderTuple } from "../../tuples/config-canvas-data-loader-tuple";
import { ModelCoordSetGridSize } from "@peek/peek_plugin_diagram/_private/tuples";
import { TriggerCanvasShapeCompileTupleAction } from "../../tuples/trigger-canvas-shape-compile-tuple-action";
import { LookupTypeE } from "@peek_admin/peek_plugin_diagram/diagram-edit-lookup-service";
import { ConfigCanvasListTuple } from "../../tuples/config-canvas-list-tuple";
import { ShapeGroupListItemTuple } from "../../tuples/config-shape-group-list-item-tuple";
import { ShapeEdgeTemplateListItemTuple } from "../../tuples/config-shape-edge-template-list-item-tuple";
import { TriggerCanvasShapeCompileResultTuple } from "../../tuples/trigger-canvas-shape-compile-result-tuple";

@Component({
    selector: "pl-diagram-config-edit-canvas",
    templateUrl: "./config-edit-canvas.component.html",
    styleUrls: ["./config-edit-canvas.component.scss"],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ConfigEditCanvasComponent
    extends NgLifeCycleEvents
    implements OnInit
{
    protected readonly LookupTypeE = LookupTypeE;

    delegate: TupleDataLoaderDelegate<ConfigCanvasDataLoaderTuple>;
    gridSizesFormControlRows$ = new BehaviorSubject<AbstractControl<any>[]>([]);

    private canvasId: number | null = null;

    protected modelSetKey$ = new BehaviorSubject<string | null>(null);
    protected coordSetKey$ = new BehaviorSubject<string | null>(null);

    protected vertexDispGroupCanvasOptions$ = new BehaviorSubject<
        ConfigCanvasListTuple[]
    >([]);
    protected vertexDispGroupNameOptions$ = new BehaviorSubject<
        ShapeGroupListItemTuple[]
    >([]);

    protected edgeDispGroupCanvasOptions$ = new BehaviorSubject<
        ConfigCanvasListTuple[]
    >([]);
    protected edgeDispGroupNameOptions$ = new BehaviorSubject<
        ShapeEdgeTemplateListItemTuple[]
    >([]);

    private unsubscribeShapeGroupCanvasSubject = new Subject<void>();
    private unsubscribeVertexShapeGroupNameSubject = new Subject<void>();
    private unsubscribeEdgeShapeGroupNameSubject = new Subject<void>();

    constructor(
        private balloonMsg: BalloonMsgService,
        private tupleService: DiagramTupleService,
        protected diagramConfigStateService: DiagramConfigStateService,
    ) {
        super();

        this.delegate = new TupleDataLoaderDelegate(
            this,
            this.tupleService.userUuid$,
        );

        // Subscribe to form changes to update the grid sizes control rows
        this.delegate.formGroup$
            .pipe(
                takeUntil(this.onDestroyEvent),
                filter((formGroup) => formGroup != null),
            )
            .subscribe((formGroup) => {
                this.updateGridSizesRows();

                // Watch for changes in the grid sizes form array
                this.gridSizesFormArray?.valueChanges
                    .pipe(
                        takeUntil(this.delegate.formGroup$.pipe(skip(1))),
                        takeUntil(this.onDestroyEvent),
                    )
                    .subscribe(() => {
                        this.updateGridSizesRows();
                    });
            });

        this.tupleService.dataLoader.addDelegate<ConfigCanvasDataLoaderTuple>(
            ConfigCanvasDataLoaderTuple.tupleName,
            this.delegate,
            this,
        );

        this.diagramConfigStateService.canvasConfigSelected$
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((canvasId: number | null) => {
                this.canvasId = canvasId;
                if (canvasId == null) {
                    this.delegate.selector$.next(null);
                } else {
                    this.delegate.selector$.next(
                        new TupleSelector(
                            ConfigCanvasDataLoaderTuple.tupleName,
                            {
                                id: canvasId,
                            },
                        ),
                    );
                }
            });

        this.delegate.data$
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((data: ConfigCanvasDataLoaderTuple | null) => {
                this.modelSetKey$.next(data?.modelSetKey);
                this.coordSetKey$.next(data?.coordSetKey);

                this.resubscribeEditDefaultCanvasOptions(
                    data?.item?.modelSetId,
                    data?.item?.id,
                );
            });
    }

    override ngOnInit(): void {
        // Component initialization logic
    }

    /**
     * Updates the grid sizes form control rows BehaviorSubject
     */
    private updateGridSizesRows(): void {
        if (this.gridSizesFormArray) {
            this.gridSizesFormControlRows$.next([
                ...this.gridSizesFormArray.controls,
            ]);
        }
    }

    /**
     * Adds a new grid size row to the form
     */
    addGridSizeRow(): void {
        if (!this.gridSizesFormArray) return;

        const newGridSize = new ModelCoordSetGridSize();
        newGridSize.coordSetId =
            this.delegate.formGroup$.getValue()?.controls["id"].value;

        this.gridSizesFormArray.push(
            ConfigCanvasDataLoaderTuple.createGridSizeFormGroup(newGridSize),
        );
    }

    /**
     * Removes a grid size row at the specified index
     */
    removeGridSizeRow(index: number): void {
        if (!this.gridSizesFormArray) return;
        this.gridSizesFormArray.removeAt(index);
    }

    /**
     * Returns the grid sizes form array
     */
    get gridSizesFormArray(): FormArray | null {
        return this.delegate.formGroup$
            .getValue()
            ?.get("gridSizes") as FormArray;
    }

    async triggerRecompile() {
        debugger;
        const action = new TriggerCanvasShapeCompileTupleAction();
        action.canvasId = this.canvasId;

        try {
            const tuples: Tuple[] =
                await this.tupleService.action.pushAction(action);
            const result = tuples[0] as TriggerCanvasShapeCompileResultTuple;

            this.balloonMsg.showSuccess(
                `${result.shapesQueued} Shapes queued for recompile,` +
                    ` and deleted ${result.gridsDeleted} grids.`,
            );
            this.balloonMsg.showInfo(
                "Watch the status tab, and wait for" +
                    " grid and disp queus to return to zero.",
            );
        } catch (e) {
            this.balloonMsg.showError(`Failed to trigger recompile: ${e}`);
        }
    }

    private resubscribeEditDefaultCanvasOptions(
        modelSetId: number | null,
        coordSetId: number | null,
    ) {
        this.unsubscribeShapeGroupCanvasSubject.next();

        if (modelSetId == null || coordSetId == null) {
            this.vertexDispGroupCanvasOptions$.next([]);
            this.vertexDispGroupNameOptions$.next([]);
            this.edgeDispGroupCanvasOptions$.next([]);
            this.edgeDispGroupNameOptions$.next([]);
            return;
        }

        this.tupleService.observer
            .subscribeToTupleSelector(
                new TupleSelector(ConfigCanvasListTuple.tupleName, {
                    modelSetId: modelSetId,
                }),
            )
            .pipe(takeUntil(this.unsubscribeShapeGroupCanvasSubject))
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((tuples: Tuple[]) => {
                this.vertexDispGroupCanvasOptions$.next(
                    (tuples as ConfigCanvasListTuple[]).filter(
                        (t) => t.dispGroupTemplatesEnabled,
                    ),
                );
                this.edgeDispGroupCanvasOptions$.next(
                    (tuples as ConfigCanvasListTuple[]).filter(
                        (t) => t.edgeTemplatesEnabled,
                    ),
                );
            });

        if (this.delegate.formGroup$.getValue() == null) {
            return;
        }

        this.delegate.formGroup$
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((formGroup: FormGroup) => {
                formGroup.controls["editDefaultVertexCoordSetId"].valueChanges
                    .pipe(takeUntil(this.onDestroyEvent))
                    .pipe(takeUntil(this.delegate.formGroup$.pipe(skip(1))))
                    .subscribe((newCanvasId) => {
                        this.resubscribeVertexShapeGroupName(newCanvasId);
                    });
            });

        this.delegate.formGroup$
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((formGroup: FormGroup) => {
                formGroup.controls["editDefaultEdgeCoordSetId"].valueChanges
                    .pipe(takeUntil(this.onDestroyEvent))
                    .pipe(takeUntil(this.delegate.formGroup$.pipe(skip(1))))
                    .subscribe((newCanvasId) => {
                        this.resubscribeEdgeShapeGroupName(newCanvasId);
                    });
            });
    }

    private resubscribeVertexShapeGroupName(coordSetId: number | null) {
        this.unsubscribeVertexShapeGroupNameSubject.next();

        if (coordSetId == null || `${coordSetId}` == "") {
            this.vertexDispGroupNameOptions$.next([]);
            return;
        }

        this.tupleService.observer
            .subscribeToTupleSelector(
                new TupleSelector(ShapeGroupListItemTuple.tupleName, {
                    coordSetId: coordSetId,
                }),
            )
            .pipe(takeUntil(this.unsubscribeVertexShapeGroupNameSubject))
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((tuples: Tuple[]) => {
                this.vertexDispGroupNameOptions$.next(
                    tuples as ShapeGroupListItemTuple[],
                );
            });
    }

    private resubscribeEdgeShapeGroupName(coordSetId: number | null) {
        this.unsubscribeEdgeShapeGroupNameSubject.next();

        if (coordSetId == null || `${coordSetId}` == "") {
            this.edgeDispGroupNameOptions$.next([]);
            return;
        }

        this.tupleService.observer
            .subscribeToTupleSelector(
                new TupleSelector(ShapeEdgeTemplateListItemTuple.tupleName, {
                    coordSetId: coordSetId,
                }),
            )
            .pipe(takeUntil(this.unsubscribeEdgeShapeGroupNameSubject))
            .pipe(takeUntil(this.onDestroyEvent))
            .subscribe((tuples: Tuple[]) => {
                this.edgeDispGroupNameOptions$.next(
                    tuples as ShapeEdgeTemplateListItemTuple[],
                );
            });
    }
}
