from fastapi import APIRouter, HTTPException, Depends, Query, Body

from botrun_flow_lang.api.user_setting_api import get_user_setting_store

from botrun_flow_lang.services.hatch.hatch_factory import hatch_store_factory

from botrun_flow_lang.services.hatch.hatch_fs_store import HatchFsStore

from botrun_hatch.models.hatch import Hatch

from typing import List

from botrun_flow_lang.services.user_setting.user_setting_fs_store import (
    UserSettingFsStore,
)

router = APIRouter()


async def get_hatch_store():
    return hatch_store_factory()


@router.post("/hatch", response_model=Hatch)
async def create_hatch(hatch: Hatch, store: HatchFsStore = Depends(get_hatch_store)):
    success, created_hatch = await store.set_hatch(hatch)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create hatch")
    return created_hatch


@router.put("/hatch/{hatch_id}", response_model=Hatch)
async def update_hatch(
    hatch_id: str, hatch: Hatch, store: HatchFsStore = Depends(get_hatch_store)
):
    existing_hatch = await store.get_hatch(hatch_id)
    if not existing_hatch:
        raise HTTPException(status_code=404, detail="Hatch not found")
    hatch.id = hatch_id
    success, updated_hatch = await store.set_hatch(hatch)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update hatch")
    return updated_hatch


@router.delete("/hatch/{hatch_id}")
async def delete_hatch(hatch_id: str, store: HatchFsStore = Depends(get_hatch_store)):
    success = await store.delete_hatch(hatch_id)
    if not success:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": f"Failed to delete hatch {hatch_id}"},
        )
    return {"success": True, "message": f"Hatch {hatch_id} deleted successfully"}


@router.get("/hatch/{hatch_id}", response_model=Hatch)
async def get_hatch(hatch_id: str, store: HatchFsStore = Depends(get_hatch_store)):
    hatch = await store.get_hatch(hatch_id)
    if not hatch:
        raise HTTPException(status_code=404, detail="Hatch not found")
    return hatch


@router.get("/hatches", response_model=List[Hatch])
async def get_hatches(
    user_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    hatch_store=Depends(get_hatch_store),
):
    hatches, error = await hatch_store.get_hatches(user_id, offset, limit)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return hatches


@router.get("/hatch/default/{user_id}", response_model=Hatch)
async def get_default_hatch(
    user_id: str, store: HatchFsStore = Depends(get_hatch_store)
):
    default_hatch = await store.get_default_hatch(user_id)
    if not default_hatch:
        raise HTTPException(status_code=404, detail="Default hatch not found")
    return default_hatch


@router.post("/hatch/set_default")
async def set_default_hatch(
    user_id: str = Body(...),
    hatch_id: str = Body(...),
    store: HatchFsStore = Depends(get_hatch_store),
):
    success, message = await store.set_default_hatch(user_id, hatch_id)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True, "message": message}


@router.get("/hatches/statistics")
async def get_hatches_statistics(
    user_setting_store: UserSettingFsStore = Depends(get_user_setting_store),
    hatch_store: HatchFsStore = Depends(get_hatch_store),
):
    """Get statistics about hatches across all users.

    Returns:
        dict: Contains total hatch count and per-user hatch counts
    """
    try:
        # Get all user IDs
        user_ids = await user_setting_store.get_all_user_ids()

        # Initialize statistics
        all_hatches = []
        total_count = 0

        # Get hatch counts for each user
        for user_id in user_ids:
            hatches, _ = await hatch_store.get_hatches(user_id)
            count = len(hatches)
            if count > 0:  # Only include users who have hatches
                all_hatches.append({"user_id": user_id, "hatches_count": count})
                total_count += count

        return {"all_hatches_count": total_count, "all_hatches": all_hatches}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch hatch statistics: {str(e)}"
        )


@router.post("/hatch/{hatch_id}/share")
async def share_hatch(
    hatch_id: str,
    user_id: str = Body(..., embed=True),
    store: HatchFsStore = Depends(get_hatch_store),
):
    """Share a hatch with another user.

    Args:
        hatch_id: ID of the hatch to share
        user_id: ID of the user to share the hatch with (in request body)

    Returns:
        dict: Success status and message
    """
    # Get the hatch to verify it exists and to get owner_id
    hatch = await store.get_hatch(hatch_id)
    if not hatch:
        raise HTTPException(status_code=404, detail="Hatch not found")

    # Share the hatch
    success, message = await store.share_hatch(hatch_id, hatch.user_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"success": True, "message": message}


@router.delete("/hatch/{hatch_id}/share/{target_user_id}")
async def unshare_hatch(
    hatch_id: str,
    target_user_id: str,
    store: HatchFsStore = Depends(get_hatch_store),
):
    """Remove sharing of a hatch with a user.

    Args:
        hatch_id: ID of the hatch to unshare
        target_user_id: ID of the user to remove sharing from

    Returns:
        dict: Success status and message
    """
    # Get the hatch to verify it exists and to get owner_id
    hatch = await store.get_hatch(hatch_id)
    if not hatch:
        raise HTTPException(status_code=404, detail="Hatch not found")

    # Unshare the hatch
    success, message = await store.unshare_hatch(
        hatch_id, hatch.user_id, target_user_id
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"success": True, "message": message}


@router.get("/hatches/shared", response_model=List[Hatch])
async def get_shared_hatches(
    user_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    store: HatchFsStore = Depends(get_hatch_store),
):
    """Get all hatches shared with a user.

    Args:
        user_id: ID of the user to get shared hatches for
        offset: Pagination offset
        limit: Maximum number of results to return

    Returns:
        List[Hatch]: List of shared hatches
    """
    hatches, error = await store.get_shared_hatches(user_id, offset, limit)
    if error:
        raise HTTPException(status_code=500, detail=error)

    return hatches


@router.get("/hatch/{hatch_id}/share/{user_id}")
async def is_hatch_shared_with_user(
    hatch_id: str,
    user_id: str,
    store: HatchFsStore = Depends(get_hatch_store),
):
    """Check if a hatch is shared with a specific user.

    Args:
        hatch_id: ID of the hatch to check
        user_id: ID of the user to check sharing with

    Returns:
        dict: Whether the hatch is shared with the user and a message
    """
    # Get the hatch to verify it exists
    hatch = await store.get_hatch(hatch_id)
    if not hatch:
        raise HTTPException(status_code=404, detail="Hatch not found")

    # Check if the hatch is shared with the user
    is_shared, message = await store.is_hatch_shared_with_user(hatch_id, user_id)

    return {"is_shared": is_shared, "message": message}
