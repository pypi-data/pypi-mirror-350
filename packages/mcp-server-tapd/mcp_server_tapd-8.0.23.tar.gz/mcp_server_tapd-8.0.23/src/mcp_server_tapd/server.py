import os
import json
import requests
import markdown
from mcp.server.fastmcp import FastMCP
from mcp_server_tapd.tapd import TAPDClient
from mcp_server_tapd.app_config import AppConfig

mcp = FastMCP("mcp-tapd")
client = TAPDClient()

@mcp.tool()
def get_stories_or_tasks(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 需求或任务，如果没有 limit 参数，则需要同时调用 get_story_count 工具获取需求数量
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_stories.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entity_type: 类型，需求stories或任务tasks（必填）
            - id: ID
            - name: 标题，支持模糊匹配，例如："%搜索词%"
            - stauts: 状态，支持枚举查询，例如：status=status1|status2|status3
            等等...
    Returns:  <str>  # 需求或者任务所有字段数据的 json 格式，返回链接给用户，链接要可点击。而且需要返回剩余的需求数量，让用户确定是否需要继续获取剩余的需求
    Note: 需求链接格式为 {tapd_base_url}/{workspace_id}/prong/stories/view/{id}
    Note: 任务链接格式为 {tapd_base_url}/{workspace_id}/prong/tasks/view/{id}
    Note: 如果没有给limit 参数，则需要提醒用户剩余的数量
    Note: 任务的状态status只有三个，open: 未开始，progressing: 进行中，done: 已完成
    """
    story_condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        story_condition.update(options)
    
    ret = client.get_stories(story_condition)
    count_ret = client.get_story_count(story_condition)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": f'{tapd_base_url}/',
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def get_story_or_task_custom_fields(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 需求或任务自定义字段配置
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entity_type: 类型，需求stories或任务tasks（必填）
    Returns:  <str>  # 需求或者任务所有自定义字段配置数据的 json 格式
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    ret = client.get_story_custom_fields(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_story_or_task_count(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 需求或者任务的数量
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_stories_count.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entity_type: 类型，需求stories或任务tasks（必填）
            - id: ID
            - name: 标题
            - workitem_type_id: 需求类别ID，支持枚举查询，例如：workitem_type_id=workitem_type_id_1|workitem_type_id_2|workitem_type_id_3
            - stauts: 状态，支持枚举查询，例如：status=status1|status2|status3
            等等...
    Returns:  <str>  # 需求所有字段数据的 json 格式
    """
    new_story = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_story.update(options)
    
    ret = client.get_story_count(new_story)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def update_story_or_task(workspace_id: int, options: dict = None) -> str:
    """更新 TAPD 需求或任务，任务的状态只有三个，open: 未开始，progressing: 进行中，done: 已完成，如果是流转需求的状态，需要调用工具先获取状态信息get_workflows_all_transitions
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/update_story.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entity_type: 类型，需求stories或任务tasks（必填）
            - id: 需求或任务ID（必填）
            - name: 标题
            - status: 状态
            - description: 描述
            等等...
    Returns: <str>,  # 需求或者任务所有字段数据的 json 格式
    Note: 需求链接格式为 {tapd_base_url}/{workspace_id}/prong/stories/view/{story_id}
    Note: 任务链接格式为 {tapd_base_url}/{workspace_id}/prong/tasks/view/{id}
    """
    new_story = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_story.update(options)
    if 'description' in new_story:
        html = markdown.markdown(new_story["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            new_story["description"] = html
    created_story = client.create_or_update_story(new_story)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": f'{tapd_base_url}/',
        "data": json.dumps(created_story, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def create_story_or_task(workspace_id: int, name: str, options: dict = None) -> dict:
    """创建 TAPD 需求
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/add_story.html
    Args:
        workspace_id: 项目ID（必填）
        name: 需求或任务的标题（必填）
        options: 可选参数字典，支持以下字段：
            - entity_type: 类型，需求stories或任务tasks（必填）
            - priority_label: 优先级
            - description: 描述，富文本格式
            等等...
    Returns:
        {
            "data": <str>,  # 需求或任务所有字段数据的 json 格式
            "url": <str>  # 需求或者任务 url，返回给用户时，链接要可点击
        }
    """
    data = {
        "workspace_id": workspace_id,
        "name": name
    }
    
    if options:
        data.update(options)
    
    if 'description' in data:
        html = markdown.markdown(data["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["description"] = html

    created_story = client.create_or_update_story(data)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    entity_type = data['entity_type']
    if entity_type == 'tasks':
        entity_id = created_story['data']['Task']['id']
    else:
        entity_id = created_story['data']['Story']['id']
    url = f'{tapd_base_url}/{workspace_id}/prong/{entity_type}/view/{entity_id}'
    return {
        "url": url, # 返回给用户时，链接要可点击
        "data": json.dumps(created_story, indent=2, ensure_ascii=False),
    }

@mcp.tool()
def get_bug(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/get_bugs.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - title: 标题
            - stauts: 状态，支持枚举查询，例如：status=status1|status2|status3
            等等...
    Returns:  <str>  # 缺陷所有字段数据的 json 格式
    Note: 缺陷链接格式为 {tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{id}
    """
    bug_condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        bug_condition.update(options)
    
    ret = client.get_bug(bug_condition)
    count_ret = client.get_bug_count(bug_condition)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def get_bug_custom_fields(workspace_id: int) -> str:
    """获取 TAPD 缺陷自定义字段配置
    Args:
        workspace_id: 项目ID（必填）
    Returns:  <str>  # 需求所有自定义字段配置数据的 json 格式
    """
    
    ret = client.get_bug_custom_fields(workspace_id)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_bug_count(workspace_id: int, options: dict = None) -> str:
    """获取 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/get_bugs_count.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: ID
            - name: 标题
            等等...
    Returns:  <str>  # 需求所有字段数据的 json 格式
    """
    new_bug = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_bug.update(options)
    
    ret = client.get_bug_count(new_bug)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def update_bug(workspace_id: int, options: dict = None) -> str:
    """更新 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/update_bug.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: 缺陷ID（必填）
            - title: 标题
            - description: 描述
            等等...
    Returns: <str>  # 缺陷所有字段数据的 json 格式
    Note: 缺陷链接格式为 {tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{id}
    """
    new_bug = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_bug.update(options)

    if 'description' in new_bug:
        html = markdown.markdown(new_bug["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            new_bug["description"] = html
    created_bug = client.create_or_update_bug(new_bug)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(created_bug, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def create_bug(workspace_id: int, title: str, options: dict = None) -> dict:
    """创建 TAPD 缺陷
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/bug/add_bug.html
    Args:
        workspace_id: 项目ID（必填）
        title: 缺陷标题（必填）
        options: 可选参数字典，支持以下字段：
            - priority_label: 优先级
            - description: 描述
            等等...
    Returns:
        {
            "data": <str>,  # 所有字段数据的 json 格式
            "url": <str>  #  url，返回给用户时，链接要可点击
        }
    Note: 缺陷链接格式为 {tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{id}
    """
    new_bug = {
        "workspace_id": workspace_id,
        "title": title
    }
    
    if options:
        new_bug.update(options)
    
    if 'description' in new_bug:
        html = markdown.markdown(new_bug["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            new_bug["description"] = html
    ret = client.create_or_update_bug(new_bug)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "url": f'{tapd_base_url}/{workspace_id}/bugtrace/bugs/view/{ret["data"]["Bug"]["id"]}', # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
    }


@mcp.tool()
def create_comments(workspace_id: int, options: dict = None) -> dict:
    """添加评论
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/comment/add_comment.html
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - entry_id: 评论所依附的业务对象实体id（必填）
            - entry_type: 评论类型（取值： bug、 bug_remark （流转缺陷时候的评论）、 stories、 tasks 。）（必填）
            - author: 评论人（必填）
            - description: 内容（必填）
            - root_id: 根评论ID
            - reply_id: 需求评论回复的ID
    Returns: <str>  # 新建评论的数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    if 'description' in data:
        html = markdown.markdown(data["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["description"] = html
    created_story = client.create_comments(data)
    return json.dumps(created_story, indent=2, ensure_ascii=False)

@mcp.tool()
def update_comments(workspace_id: int, options: dict = None) -> dict:
    """更新评论，返回更新评论的数据
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: 评论id（必填）
            - description: 内容（必填）
            - change_creator: 变更人（必填）
    Returns: <str>  # 更新后的评论数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    if 'description' in data:
        html = markdown.markdown(data["description"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["description"] = html
    created_story = client.create_comments(data)
    return json.dumps(created_story, indent=2, ensure_ascii=False)

@mcp.tool()
def get_comments(workspace_id: int, options: dict = None) -> dict:
    """获取符合查询条件的所有评论（分页显示，默认一页30条）
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: 评论ID（格式如：1159271484001002933）
            - title: 标题
            - description: 内容
            - author: 评论人
            - entry_type: 评论类型（取值： bug、 bug_remark （流转缺陷时候的评论）、 stories、 tasks 。多个类型间以竖线隔开）
            - entry_id: 评论所依附的业务对象实体id
            - created: 创建时间，支持时间查询
            - limit: 设置返回数量限制，默认为30
            - page: 返回当前数量限制下第N页的数据，默认为1（第一页）
            - order: 排序规则，规则：字段名 ASC或者DESC，然后 urlencode，如按创建时间逆序：order=created%20desc
            - fields: 设置获取的字段，多个字段间以','逗号隔开
    Returns: <str>  # 符合条件的评论数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_comments(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_all_transitions(workspace_id: int, options: dict = None) -> dict:
    """获取项目下的工作流流转细则，例如要流转到"实现中"，则需要调用这个工具查看当前状态能流转到的状态
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别ID（必填）
    Returns: <str>  状态流转细则
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_all_transitions(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_status_map(workspace_id: int, options: dict = None) -> dict:
    """获取工作流状态中英文名对应关系，例如想要获取所有"实现中"的需求/缺陷等，可以调用这个接口先获取状态的英文名，再根据这个英文名作为 status 字段的值去查询
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别ID（必填）
    Returns: <str>  状态流转细则
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_status_map(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workitem_types(workspace_id: int, options: dict = None) -> dict:
    """获取符合查询条件的所有需求类别（分页显示，默认一页30条）
    TAPD API 文档：https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/api_reference/story/get_workitem_types.html
    Args:
        workspace_id: 项目ID（必填）
        options:
            - id: id，支持多ID查询
            - name: 需求类别名称
            等等...
    Returns: <str>  项目下所有需求类别字段数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workitem_types(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workflows_last_steps(workspace_id: int, options: dict = None) -> dict:
    """获取工作流结束状态，一次只能获取一个项目的工作流结束状态
    Args:
        workspace_id: 项目ID（必填）
        options:
            - system: 系统名。取 bug （缺陷的）或者 story（需求的）（必填）
            - workitem_type_id: 需求类别id（不传则取项目下所有工作流的结束状态）
            - type: 节点类型，仅并行工作流需区分。status 状态，step 并行工作流节点。默认只返回结束状态。若需要同时返回结束状态和结束节点，支持数组type[]=status&type[]=step
    Returns: <str> 工作流结束状态
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    ret = client.get_workflows_last_steps(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_custom_fields_settings(workspace_id: int) -> dict:
    """获取需求自定义字段配置，一次只能获取一个项目的配置
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 需求自定义字段配置
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_custom_fields_settings(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_fields_lable(workspace_id: int) -> dict:
    """获取需求所有字段的中英文
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_fields_lable(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_stories_fields_info(workspace_id: int) -> dict:
    """获取需求所有字段及候选值，返回符合查询条件的所有需求字段及候选值。 部分字段为静态候选值，建议参考下方 "可选值说明"部分。其余动态字段（如：status(状态)/iteration_id(迭代)/categories(需求分类)），需要通过该接口获取对应的候选值（中英文映射）
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_stories_fields_info(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_workspace_info(workspace_id: int) -> dict:
    """根据项目ID（workspace_id）获取项目信息，包含项目ID,项目名称,状态,创建时间,创建人等信息
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_workspace_info(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_iterations(workspace_id: int, options: dict = None) -> dict:
    """根据项目ID（workspace_id）获取符合查询条件的所有迭代，例如可以通过名称获取迭代 id，然后作为iteration_id字段的值获取到迭代下的需求或缺陷
    Args:
        workspace_id: 项目ID（必填）
        options:
            - id: ID
            - name: 标题
            - startdate: 开始时间
            - enddate: 结束时间
            ...
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.get_iterations(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)
    
@mcp.tool()
def update_iteration(workspace_id: int, options: dict = None) -> dict:
    """更新迭代，返回更新迭代的数据
    Args:
        workspace_id: 项目ID（必填）
        options:
            - id: 迭代ID（必填）
            - current_user: 变更人（必填）
            - name: 标题
            - startdate: 开始时间
            - enddate: 结束时间
            - creator: 创建人
            - status: 状态
            ...
    Returns: <str> # 迭代所有字段数据的 json 格式
    Note: 迭代字段说明 status: 迭代状态，open: 开启，done: 已关闭
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.create_or_update_iteration(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def create_iteration(workspace_id: int, options: dict = None) -> dict:
    """创建迭代，返回创建迭代的数据
    Args:
        workspace_id: 项目ID（必填）
        options:
            - name: 迭代名称（必填）
            - startdate: 开始时间（必填）
            - enddate: 结束时间（必填）
            - creator: 创建人（必填）
            - status: 状态
            ...
    Returns: <str> # 迭代所有字段数据的 json 格式，需要返回链接给用户，链接要可点击。
    Note: 迭代字段说明 status: 迭代状态，open: 开启，done: 已关闭
    Note: 迭代链接格式为 {tapd_base_url}/{workspace_id}/prong/iterations/card_view/{id}
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.create_or_update_iteration(data)

    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "url": f'{tapd_base_url}/{workspace_id}/prong/iterations/card_view/{ret["data"]["Iteration"]["id"]}', # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
    }

@mcp.tool()
def get_related_bugs(workspace_id: int, options: dict = None) -> dict:
    """获取符合查询条件的所有需求关联的缺陷ID
    Args:
        workspace_id: 项目ID（必填）
        options:
            - story_id: ID（必填），支持多ID查询
    Returns: <str> 
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.get_related_bugs(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def entity_relations(workspace_id: int, options: dict = None) -> dict:
    """创建需求与缺陷关联关系
    Args:
        workspace_id: 所属TAPD项目ID（必填）
        options:
            - source_type: 关联关系源对象类型（story、bug）（必填）
            - target_type: 关联关系目标对象类型（story、bug）（必填）
            - source_id: 关联关系源对象id（必填）
            - target_id: 关联关系目标对象id（必填）
    Returns: <str> # 返回关联关系
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.add_entity_relations(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def create_or_update_tcases(workspace_id: int, options: dict = None) -> dict:
    """新建测试用例，返回新建测试用例的数据
    Args:
        workspace_id(int): 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id(int): 测试用例 ID
            - name(str): 用例名称
            - category_id: 用例目录 enum('updating','abandon','normal')
            - status: 前置条件
            - precondition: 前置条件
            - steps: 用例步骤
            - expectation: 预期结果
            - type: 用例类型
            - priority: 用例等级
            - creator: 创建人
            - custom_field_*: 自定义字段参数，具体字段名通过接口 获取测试用例自定义字段配置获取
    Returns: <str>  # 新建测试用例的数据
    Note: 测试用例链接格式为 {tapd_base_url}/{workspace_id}/sparrow/tcase/view/{id}
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    
    if 'precondition' in data:
        html = markdown.markdown(data["precondition"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["precondition"] = html
    if 'steps' in data:
        html = markdown.markdown(data["steps"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["steps"] = html
    if 'expectation' in data:
        html = markdown.markdown(data["expectation"], extensions=['extra', 'codehilite', 'toc'])
        if '<p>' in html or '<h' in html or '<ul>' in html or '<ol>' in html:
            data["expectation"] = html
    created_tcases = client.create_tcases(data)
    return json.dumps(created_tcases, indent=2, ensure_ascii=False)

@mcp.tool()
def get_tcases(workspace_id: int, options: dict = None) -> str:
    """获取测试用例，返回符合查询条件的所有测试用例（分页显示，默认一页30条），默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页
    Args:
        workspace_id(int): 项目ID（必填）
        options: 可选参数，支持以下字段：
            - id(str): ID
            - name: 用例名称
            - steps: 用例步骤
            - category_id(int): 用例目录
            - created: 创建时间
            - modifier: 最后修改人
            - modified: 最后修改时间
            - creator: 创建人
            - status: 用例状态 enum('updating','abandon','normal')	
            - precondition: 前置条件
            - expectation: 预期结果
            - type: 用例类型
            - priority: 用例等级
            - is_automated: 是否实现自动化
            - automation_type: 自动化测试类型
            - automation_platform: 自动化测试平台
            - is_serving: 是否上架
            - limit: 设置返回数量限制，默认为30
            - page: 返回当前数量限制下第N页的数据，默认为1（第一页）
            - order: 排序规则，规则：字段名 ASC或者DESC，然后 urlencode，如按创建时间逆序：order=created%20desc
            - fields: 设置获取的字段，多个字段间以','逗号隔开
            - custom_field_*: 自定义字段参数，具体字段名通过接口 获取
    Returns:  <str>  # 符合查询条件的测试用例所有字段数据的 json 格式
    Note: 测试用例链接格式为 {tapd_base_url}/{workspace_id}/sparrow/tcase/view/{id}
    """
    condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        condition.update(options)
    
    ret = client.get_tcases(condition)
    count_ret = client.get_tcases_count(condition)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def create_wiki(workspace_id: int, options: dict = None) -> dict:
    """新建Wiki，返回新建Wiki的数据
    Args:
        workspace_id(int): 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - name(str): 标题（必填）
            - markdown_description: wiki 内容，Markdown 格式
            - creator: 创建人（必填）
            - note: 备注
            - parent_wiki_id(str): 父wiki名
    Returns: <str>  # 新建wiki的数据
    Note: wiki链接格式为 {tapd_base_url}/{workspace_id}/markdown_wikis/show/#{id}
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    if options:
        data.update(options)
    created_wiki = client.create_wiki(data)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(created_wiki, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def update_wiki(workspace_id: int, options: dict = None) -> str:
    """更新 TAPD wiki
    Args:
        workspace_id: 项目ID（必填）
        options: 可选参数字典，支持以下字段：
            - id: wiki ID（必填）
            - name(str): 标题
            - markdown_description: wiki 内容，Markdown 格式
            - note: 备注
            - parent_wiki_id(str): 父wiki名
    Returns: <str>  # wiki 所有字段数据的 json 格式
    Note: wiki链接格式为 {tapd_base_url}/{workspace_id}/markdown_wikis/show/#{id}
    """
    new_wiki = {
        "workspace_id": workspace_id,
    }
    
    if options:
        new_wiki.update(options)

    updated_wiki = client.create_wiki(new_wiki)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(updated_wiki, indent=2, ensure_ascii=False)
    }

@mcp.tool()
def get_wiki(workspace_id: int, options: dict = None) -> str:
    """获取 Wiki，返回符合查询条件的所有Wiki（分页显示，默认一页30条）
    Args:
        workspace_id(int): 项目ID（必填）
        options: 可选参数，支持以下字段：
            - id(int): id
            - name(str): 标题
            - modifier(str): 最后修改人
            - creator: 创建人
            - note: 备注
            - view_count: 浏览量
            - created: 创建时间
            - modified: 最后修改时间	
            - limit: 设置返回数量限制，默认为30	
            - page: 返回当前数量限制下第N页的数据，默认为1（第一页）	
            - order(str): 排序规则，规则：字段名 ASC或者DESC，然后 urlencode，如按创建时间逆序：order=created%20desc
            - fields: 设置获取的字段，多个字段间以','逗号隔开	
    Returns:  <str>  # 符合查询条件的wiki所有字段数据的 json 格式
    Note: wiki链接格式为 {tapd_base_url}/{workspace_id}/markdown_wikis/show/#{id}
    """
    condition = {
        "workspace_id": workspace_id,
    }
    
    if options:
        condition.update(options)
    
    ret = client.get_wiki(condition)
    count_ret = client.get_wiki_count(condition)
    config = AppConfig()
    if config.tapd_base_url is None:
        tapd_base_url = os.getenv("TAPD_BASE_URL")
    else:
        tapd_base_url = config.tapd_base_url
    return {
        "base_url": {tapd_base_url}, # 返回给用户时，链接要可点击
        "data": json.dumps(ret, indent=2, ensure_ascii=False),
        "count": json.dumps(count_ret, indent=2, ensure_ascii=False)
    }


@mcp.tool()
def get_tcases_custom_fields_settings(workspace_id: int) -> dict:
    """获取测试用例自定义字段配置
    Args:
        workspace_id: 项目ID（必填）
    Returns: <str> 测试用例自定义字段配置
    """
    data = {
        "workspace_id": workspace_id,
    }
    
    ret = client.get_tcases_custom_fields_settings(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)
@mcp.tool()
def get_todo(entity_type: str, user_nick: str = None) -> dict:
    """获取用户的待办
    Args:
        entity_type: 业务对象类型，如需求story、缺陷bug、任务task（必填）
        user_nick: 用户昵称，如果为空则从环境变量CURRENT_USER_NICK获取
    Returns: 
        dict: 待办数据
    Raises:
        ValueError: 当user_nick为空且环境变量CURRENT_USER_NICK也为空时抛出
    """
    if not entity_type:
        raise ValueError("entity_type is required")
        
    if not user_nick:
        user_nick = os.getenv("CURRENT_USER_NICK")
        if not user_nick:
            raise ValueError("user_nick is required but neither parameter nor environment variable CURRENT_USER_NICK is set")
    
    data = {
        "entity_type": entity_type,
        "user_nick": user_nick,
    }
    
    ret = client.get_todo(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def add_timesheets(workspace_id: int, options: dict = None) -> dict:
    """填写花费工时，返回新建花费工时的数据，可以先用get_timesheets查下owner是否在spentdate已经填写过花费，如果spentdate日期已存在花费记录，则需要调用update_timesheets进行更新
    Args:
        workspace_id: TAPD 项目 ID（必填）
        options:
            - entity_type: 对象类型，如story、task、bug（必填）
            - entity_id: 对象ID（必填）
            - timespent: 花费工时（必填）
            - owner: 花费创建人（必填）
            - spentdate: 花费日期，格式为 YYYY-MM-DD
            - memo: 花费描述
            - timeremain: 剩余工时
    Returns: <str> # 返回新建花费工时的数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.update_timesheets(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def update_timesheets(workspace_id: int, options: dict = None) -> dict:
    """更新花费工时，返回花费工时更新后的数据，每次只允许更新一条数据
    Args:
        workspace_id: TAPD 项目 ID（必填）
        options:
            - id: 花费id
            - timespent: 花费工时（必填）
            - timeremain: 剩余工时
            - memo: 花费描述
    Returns: <str> # 返回花费工时更新后的数据
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.update_timesheets(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def get_timesheets(workspace_id: int, options: dict = None) -> dict:
    """获取花费工时，返回符合查询条件的所有花费工时（分页显示，默认一页30条）默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页
    Args:
        workspace_id: TAPD 项目 ID（必填）
        options:
            - id: 花费id
            - entity_type: 对象类型，如story、task、bug
            - entity_id: 对象ID
            - timespent: 花费工时
            - spentdate: 花费日期，格式为 YYYY-MM-DD
            - modified: 最后修改时间
            - owner: 花费创建人
            - include_parent_story_timesheet: 值=0不返回父需求的花费
            - created: 创建时间
            - memo: 花费描述
            - is_delete: 是否已删除。默认取 0，不返回已删除的工时记录。取 1 可以返回已删除的记录
            - limit: 设置返回数量限制，默认为30
            - page: 返回当前数量限制下第N页的数据，默认为1（第一页）
            - order: 排序规则，规则：字段名 ASC或者DESC，然后 urlencode，如按创建时间逆序：order=created%20desc
            - fields: 设置获取的字段，多个字段间以','逗号隔开
    Returns: <str> # 返回符合查询条件的所有花费工时（分页显示，默认一页30条
    """
    data = {
        "workspace_id": workspace_id,
    }
    if options:
        data.update(options)
    ret = client.get_timesheets(data)
    return json.dumps(ret, indent=2, ensure_ascii=False)

@mcp.tool()
def send_qiwei_message(msg: str) -> dict:
    """发送信息到企业微信群
    Args:
        msg: 推送的企业微信的信息，Markdown 格式（必填）
    Returns: <str> 
    """
    data = {
        "msg": msg,
    }
    return client.send_message(data)

def main():
    config = AppConfig()
    if config.mode == "http":
        mcp.run(transport="sse")
    else:
        mcp.run()

if __name__ == "__main__":
    config = AppConfig()
    if config.mode == "http":
        mcp.run(transport="sse")
    else:
        mcp.run()