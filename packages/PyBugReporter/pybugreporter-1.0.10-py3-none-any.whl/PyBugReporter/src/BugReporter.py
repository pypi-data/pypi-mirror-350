import asyncio
import sys
import traceback
from functools import wraps
from PyBugReporter.src.DiscordBot import DiscordBot

from python_graphql_client import GraphqlClient

class NotCreatedError(Exception):
    """Raised when someone tries to report a bug to a repo that has not been set up as a reporting destination through setVars.
    """
    pass

class BugHandler:
    """A class for catching exceptions and automatically creating issues on a GitHub repo.

    Attributes:
        githubKey (str): the key used to make bug reports to our github
        repoName (str): the name of the repository
        orgName (str): the name of the organization
        test (bool): whether to run in testing mode
        extraInfo (bool): whether to include extra information in the bug report
        kwargs: extra info for the bug report
    """
    githubKey: str = ''
    repoName: str = ''
    orgName: str = ''
    test: bool = False
    useDiscord: bool = False
    botToken: str = ''
    channelId: str | int = ''

    def __init__(self, githubKey: str, repoName: str, orgName: str, test: bool, useDiscord: bool = False, botToken: str = "", channelId: str | int = "") -> None:
        """Saves the given information in the BugHandler object.

        Args:
            githubKey (str): the key to use to make the issue
            repoName (str): the name of the repo to report to
            orgName (str): the organization of the repo
            test (bool): whether or not bugs in this code should actually be reported
            useDiscord (bool): whether to send the bug report to Discord
            botToken (str): the token for the Discord bot
            channelId (str | int): the ID of the Discord channel to send messages to
        """
        self.githubKey = githubKey
        self.repoName = repoName
        self.orgName = orgName
        self.test = test
        self.useDiscord = useDiscord

        if useDiscord:
            self.botToken = botToken
            self.channelId = channelId

class BugReporter:
    """Sends errors to their corresponding repos.

    Attributes:
        handlers (dict): the created BugHandlers to use to send reports
        extraInfo (bool): whether or not extra information is being passed in
        repoName (str): the most recent set up repo to send to
    """
    handlers: dict = {}
    extraInfo: bool = False
    repoName: str

    def __init__(self, repoName: str, extraInfo: bool, **kwargs) -> None:
        """Initializes the BugReporter class as a decorator.
        
        Args:
            extraInfo (bool): whether to include extra information in the bug report
            **kwargs: extra info for the bug report
        """
        self.repoName = repoName
        self.extraInfo = extraInfo
        self.kwargs = kwargs

    @classmethod
    def setVars(cls, githubKey: str, repoName: str, orgName: str, test: bool, useDiscord: bool = False, botToken: str = "", channelId: str = "") -> None:
        """Sets the necessary variables to make bug reports.

        Args:
            githubKey (str): the key used to make bug reports to our github
            repoName (str): the name of the repository
            orgName (str): the name of the organization
            test (bool): whether to run in testing mode
        """
        cls.handlers[repoName] = BugHandler(githubKey, repoName, orgName, test, useDiscord, botToken, channelId)

    def __call__(self, func: callable) -> None:
        """Decorator that catches exceptions and sends a bug report to the github repository.

        Args:
            func (callable): the function to be decorated
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            """Wrapper function that catches exceptions and sends a bug report to the github repository.

            Args:
                *args: the arguments for the function
                **kwargs: the keyword arguments for the function
            """
            repoName = self.repoName
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self._handleError(e, repoName, *args, **kwargs)
        return wrapper

    def _handleError(self, e: Exception, repoName: str, *args, **kwargs) -> None:
        """Handles error by creating a bug report.

        Args:
            e (Exception): the exception that was raised

        Raises:
            e: the exception that was raised
        """
        excType = type(e).__name__
        tb = traceback.extract_tb(sys.exc_info()[2])
        functionName = tb[-1][2]

        # title for bug report
        title = f"{repoName} had a {excType} error with the {functionName} function"

        # description for bug report
        description = f'Type: {excType}\nError text: {e}\nFunction Name: {functionName}\n\n{traceback.format_exc()}'
        description += f"\nArguments: {args}\nKeyword Arguments: {kwargs}"
        if self.extraInfo:
            description += f"\nExtra Info: {self.kwargs}"

        # shortened description for discord if too long (shortens the error text)
        start = f"# {title}\n\nType: {excType}\nError text: "
        compress = f"{e}\nTraceback: {traceback.format_exc()}"
        end = f"\n\nFunction Name: {functionName}\nArguments: {args}\nKeyword Arguments: {kwargs}"
        if self.extraInfo:
            end += f"\nExtra Info: {self.kwargs}"

        staticLength = len(start) + len(end)
        if staticLength > 2000:
            shortDescription = f"# {title}\n\n" + description[:2000 - len(f"# {title}\n\n") - 3] + "..."
        else:
            shortDescription = f"{start}{compress[:2000 - staticLength]}{end}"

        print(f"SHORT DESCRIPTION with length {len(shortDescription)}:\n{shortDescription}")
        

        # Check if we need to send a bug report
        if not self.handlers[repoName].test:
            self._sendBugReport(repoName, title, description, shortDescription)

        print(title)
        print(description)
        raise e

    def _sendBugReport(self, repoName: str, errorTitle: str, errorMessage: str, shortErrorMessage: str) -> None:
        """Sends a bug report to the Github repository.

        Args:
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """ 
        asyncio.run(self._sendBugReport_async(repoName, errorTitle, errorMessage, shortErrorMessage))
   
    async def _sendBugReport_async(self, repoName: str, errorTitle: str, errorMessage: str, shortErrorMessage: str) -> None:
        """Sends a bug report to the Github repository asynchronously.
        
        Args:
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.handlers[repoName].githubKey}"}

        # query variables
        repoId = await self._getRepoId_async(self.handlers[repoName])
        bugLabel = "LA_kwDOJ3JPj88AAAABU1q15w"
        autoLabel = "LA_kwDOJ3JPj88AAAABU1q2DA"
        
        # Create new issue
        createIssue = """
            mutation createIssue($input: CreateIssueInput!) {
                createIssue(input: $input) {
                    issue {
                        id
                        title                
                        body
                        repository {
                            name
                        }
                        labels(first: 10) {
                            nodes {
                            name
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "input": {
                "repositoryId": repoId,
                "title": errorTitle,
                "body": errorMessage,
                "labelIds": [bugLabel, autoLabel]
            }
        }

        issueExists = await self._checkIfIssueExists_async(self.handlers[repoName], errorTitle)

        # Send to Discord if applicable
        if self.handlers[repoName].useDiscord:
            discordBot = DiscordBot(self.handlers[repoName].botToken, self.handlers[repoName].channelId)
            await discordBot.send_message(shortErrorMessage, issueExists)

        if (not issueExists):
            result = await client.execute_async(query=createIssue, variables=variables, headers=headers)
            print('\nThis error has been reported to the Tree Growth team.\n')

            issueId = result['data']['createIssue']['issue']['id']  # Extract the issue ID

            # Mutation to add issue to a project
            addToProject = """
                mutation addToProject($projectId: ID!, $contentId: ID!) {
                    addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                        item {
                            id
                        }
                    }
                }
            """
            
            # Replace with your actual project ID
            projectId = await self.getProjectId_async(repoName, "Tree Growth Projects")

            variables = {
                "projectId": projectId,
                "contentId": issueId
            }
            
            # Execute the mutation to add the issue to the project
            await client.execute_async(query=addToProject, variables=variables, headers=headers)
        else:
            print('\nOur team is already aware of this issue.\n')

    async def getProjectId_async(self, repoName: str, projectName: str) -> str:
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {self.handlers[repoName].githubKey}"}

        # Define the GraphQL query to list projects for the repository
        query = """
            query getProjectId($owner: String!, $repo: String!) {
                repository(owner: $owner, name: $repo) {
                    projectsV2(first: 10) {
                        nodes {
                            id
                            title
                        }
                    }
                }
            }
        """
        
        variables = {
            "owner": self.handlers[repoName].orgName,
            "repo": repoName
        }

        # Execute the query
        response = await client.execute_async(query=query, variables=variables, headers=headers)
        projects = response["data"]["repository"]["projectsV2"]["nodes"]

        # Find the project with the matching name and return its ID
        for project in projects:
            if project["title"] == projectName:
                return project["id"]

        raise ValueError(f"Project '{projectName}' not found in repository '{repoName}'.")

    async def _checkIfIssueExists_async(self, handler: BugHandler, errorTitle: str) -> bool:
        """Checks if an issue already exists in the repository.

        Args:
            handler (BugHandler): the object of reporting details
            errorTitle (str): the title of the error

        Returns:
            bool: True if the issue exists, False if it does not
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

        # query variables
        autoLabel = "auto generated"

        # Query to return all issues with auto gen label
        findIssue = """
            query findIssue ($login: String = "", $name: String = "", $labels: [String!] = "") {
                organization(login: $login) {
                    repository(name: $name) {
                        issues(labels: $labels, first: 10, states: [OPEN]) {
                            nodes {
                                title,
                                state
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "login": handler.orgName,
            "name": handler.repoName,
            "labels": autoLabel,
        }

        result = await client.execute_async(query=findIssue, variables=variables, headers=headers)
        nodes = result['data']['organization']['repository']['issues']['nodes']

        index = 0
        issueExists = False

        while (len(nodes) > index) :
            title = nodes[index]['title']
            if (errorTitle == title) :
                issueExists = True
                break
            else:
                index += 1

        return issueExists

    async def _getRepoId_async(self, handler: BugHandler) -> str:
        """Gets the repository ID.

        Args:
            handler (BugHandler): the object of reporting details

        Returns:
            str: the repository ID
        """
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

        # query variables
        getID = """
            query getID($owner: String!, $name: String!) {
                repository(owner: $owner, name: $name) {
                    id
                }
            }
        """

        variables = {
            "owner": handler.orgName,
            "name": handler.repoName
        }

        repoID = await client.execute_async(query=getID, variables=variables, headers=headers)
        return repoID['data']['repository']['id']

    @classmethod
    def manualBugReport(cls, repoName: str, errorTitle: str, errorMessage: str) -> None:
        """Manually sends a bug report to the Github repository.

        Args:
            repoName (str): the name of the repo to report to
            errorTitle (str): the title of the error
            errorMessage (str): the error message
        """
        if repoName not in cls.handlers:
            raise NotCreatedError(f"{repoName} has not been associated with a reporter")
        handler = cls.handlers[repoName]
        if handler.test == True:
            print('This is a test run and no bug report will be sent.')
            return
        client = GraphqlClient(endpoint="https://api.github.com/graphql")
        headers = {"Authorization": f"Bearer {handler.githubKey}"}

        # query variables
        repoId = cls._getRepoId(cls, handler)
        bugLabel = "LA_kwDOJ3JPj88AAAABU1q15w"
        autoLabel = "LA_kwDOJ3JPj88AAAABU1q2DA"
        
        # Create new issue
        createIssue = """
            mutation createIssue($input: CreateIssueInput!) {
                createIssue(input: $input) {
                    issue {
                        title                
                        body
                        repository {
                            name
                        }
                        labels(first: 10) {
                            nodes {
                            name
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "input": {
                "repositoryId": repoId,
                "title": errorTitle,
                "body": errorMessage,
                "labelIds": [bugLabel, autoLabel]
            }
        }

        issueExists = cls._checkIfIssueExists(cls, handler, errorTitle)

        if (issueExists == False):
            result = asyncio.run(client.execute_async(query=createIssue, variables=variables, headers=headers))
            print('\nThis error has been reported to the Tree Growth team.\n')
        else:
            print('\nOur team is already aware of this issue.\n')
