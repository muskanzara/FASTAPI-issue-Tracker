import uuid
from fastapi import APIRouter , HTTPException , status
from app.schemas import IssueOut , IssueCreate, IssueStatus , IssueUpdate

router = APIRouter( prefix = "/api/v1/issues", tags=["issues"])

@router.get("/" , response_model=list[IssueOut])
async def get_issues():
    """Retrieve all issues."""
    issues = load_data()
    return issues


@router.post("/" , response_model=IssueOut , status_code= status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    """create new issue."""
    issues = load_data()

    new_issue = IssueOut (
        id = str(uuid.uuid4()),
        title = payload.title,
        description = payload.description,
        priority= payload.priority,
        status=  IssueStatus.open,
    )

    issues.append(new_issue)
    save_data(issues)
    return new_issue


@router.get("/{issue_id}" , response_model=IssueOut)
def get_issue(issue_id : str):
    """Retrieve a specific issue by ID."""
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Isuue not found")


@router.put("/{issue_id}" , response_model=IssueOut)
def update_issue(issue_id : str , payload : IssueUpdate):

    """Update an existing issue."""
    issues= load_data()
    for index, issue in enumerate(issues):
        if issue["id"]== issue_id:
            update_issue = issue.copy()
            if payload.title is not None:
                update_issue["title"] = payload.title
            if payload.description is not None:
                update_issue["description"] = payload.description
            if payload.priority is not None:
                update_issue["priority"] = payload.priority
            if payload.status is not None:
                update_issue["status"] = payload.status
            issues[index]= update_issue
            save_data(issues)
            return update_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUN , detail= "Issue not found")


@router.delete("/{issue_id}" , status_code=status.HTTP_204_NO_CONTENT)
def DELETE_issue(issue_id : str):
    """Delete an issue by ID."""
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:
            issue.pop(index)
            save_data(issues)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
          detail="Isuue not found"
    )
