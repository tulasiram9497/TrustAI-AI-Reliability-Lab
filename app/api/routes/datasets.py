from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.datasets.loader import load_dataset

router = APIRouter(prefix="/api/v1")
DATASET_STORE: dict[str, dict[str, Any]] = {}


@router.post("/datasets")
def create_dataset(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        dataset = load_dataset(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    DATASET_STORE[dataset.dataset_id] = {
        "dataset_id": dataset.dataset_id,
        "name": dataset.name,
        "case_count": dataset.case_count,
        "cases": [case.model_dump(mode="json") for case in dataset.cases],
    }
    return {"dataset_id": dataset.dataset_id, "case_count": dataset.case_count}


@router.get("/datasets")
def list_datasets(limit: int = Query(default=50, ge=1, le=200)) -> dict[str, Any]:
    items = [{"dataset_id": dataset_id, **payload} for dataset_id, payload in list(DATASET_STORE.items())[:limit]]
    return {"items": items, "count": len(items)}


@router.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: str) -> dict[str, Any]:
    dataset = DATASET_STORE.get(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset
