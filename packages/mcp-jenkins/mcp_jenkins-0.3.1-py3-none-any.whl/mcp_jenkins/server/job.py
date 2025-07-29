from mcp.server.fastmcp import Context

from mcp_jenkins.server import client, mcp


@mcp.tool()
async def get_all_jobs(ctx: Context) -> list[dict]:
    """
    Get all jobs from Jenkins

    Returns:
        list[dict]: A list of all jobs
    """
    return [job.model_dump(exclude_none=True) for job in client(ctx).job.get_all_jobs()]


@mcp.tool()
async def get_job_config(ctx: Context, fullname: str) -> str:
    """
    Get specific job config from Jenkins

    Args:
        fullname: The fullname of the job

    Returns:
        str: The config of the job
    """
    return client(ctx).job.get_job_config(fullname)


@mcp.tool()
async def search_jobs(
    ctx: Context,
    class_pattern: str = None,
    name_pattern: str = None,
    fullname_pattern: str = None,
    url_pattern: str = None,
    color_pattern: str = None,
) -> list[dict]:
    """
    Search job by specific field

    Args:
        class_pattern: The pattern of the _class
        name_pattern: The pattern of the name
        fullname_pattern: The pattern of the fullname
        url_pattern: The pattern of the url
        color_pattern: The pattern of the color

    Returns:
        list[dict]: A list of all jobs
    """
    return [
        job.model_dump(exclude_none=True)
        for job in client(ctx).job.search_jobs(
            class_pattern=class_pattern,
            name_pattern=name_pattern,
            fullname_pattern=fullname_pattern,
            url_pattern=url_pattern,
            color_pattern=color_pattern,
        )
    ]


@mcp.tool()
async def get_job_info(ctx: Context, fullname: str) -> dict:
    """
    Get specific job info from Jenkins

    Args:
        fullname: The fullname of the job

    Returns:
        dict: The job info
    """
    return client(ctx).job.get_job_info(fullname).model_dump(exclude_none=True)
