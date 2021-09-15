SELECT *
FROM PortfolioProject..CovidDeaths
Where continent is not null
ORDER BY 3,4

--SELECT *
--FROM PortfolioProject..CovidVaccinations
--ORDER BY 3,4

Select Location, date, total_cases, new_cases, total_deaths, population
FROM PortfolioProject..CovidDeaths
ORDER BY 1, 2


-- Death as Percentage of Cases

Select Location, date, total_cases, total_deaths, (total_deaths/total_cases) * 100 as Death_Percentage
FROM PortfolioProject..CovidDeaths
Where location like '%states%'
ORDER BY 1, 2

-- Total Cases V. Population

Select Location, date, total_cases, Population, (total_cases/Population) * 100 as Population_Percentage
FROM PortfolioProject..CovidDeaths
Where location like '%states%'
ORDER BY 1, 2


-- Highest Infection Rate as Percentage of Population

Select Location, Population, MAX(total_cases)as Max_Infection_Count, Max((total_cases/Population)) * 100 as Percent_Pop_Infected
FROM PortfolioProject..CovidDeaths
Group By Location, Population
ORDER BY Percent_Pop_Infected desc

-- Highest Death Count

Select Location, MAX(cast(Total_Deaths as int)) as Total_death_count
FROM PortfolioProject..CovidDeaths
Where continent is not null
Group By Location
ORDER BY Total_death_count desc

-- Highest Death Count by Continent

Select Continent, MAX(cast(Total_Deaths as int)) as Total_death_count
FROM PortfolioProject..CovidDeaths
Where continent is not null
Group By Continent
order by Total_death_count desc

-- Corrected Continet Counts

Select location, MAX(cast(Total_Deaths as int)) as Total_death_count
FROM PortfolioProject..CovidDeaths
Where continent is null
Group By location
order by Total_death_count desc

-- GLOBAL NUMBERS

Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases) * 100 as Death_Percentage
FROM PortfolioProject..CovidDeaths
-- Where location like '%states%'
Where continent is not null
--Group By date
ORDER BY 1, 2


-- Total Vaccination V. Population

Select dea.continent, dea.location, dea.date, dea.population, vax.new_vaccinations, 
	SUM(cast(vax.new_vaccinations as int)) OVER (Partition By dea.Location Order By dea.location, dea.date)
	as Rolling_Vax_Count
FROM PortfolioProject..CovidDeaths dea 
Join PortfolioProject..CovidVaccinations vax
	On dea.location = vax.location 
	and dea.date = vax.date
where dea.continent is not null
order by 2,3

-- USING CTE

WITH Pop_v_vax (Continent, Location, Date, Population, New_Vaccinations, Rolling_Vax_Count)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vax.new_vaccinations, 
	SUM(cast(vax.new_vaccinations as int)) OVER (Partition By dea.Location Order By dea.location, dea.date)
	as Rolling_Vax_Count
FROM PortfolioProject..CovidDeaths dea 
Join PortfolioProject..CovidVaccinations vax
	On dea.location = vax.location 
	and dea.date = vax.date
where dea.continent is not null
--order by 2,3
)
SELECT * , (Rolling_Vax_Count/Population) * 100
FROM Pop_v_vax

-- USING TEMP TABLE

Drop Table if Exists #PercentPopVaccinated
Create Table #PercentPopVaccinated
(
Continent nvarchar(255),
location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
Rolling_Vax_Count numeric
)

Insert into #PercentPopVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vax.new_vaccinations, 
	SUM(cast(vax.new_vaccinations as int)) OVER (Partition By dea.Location Order By dea.location, dea.date)
	as Rolling_Vax_Count
FROM PortfolioProject..CovidDeaths dea 
Join PortfolioProject..CovidVaccinations vax
	On dea.location = vax.location 
	and dea.date = vax.date
where dea.continent is not null
--order by 2,3
SELECT * , (Rolling_Vax_Count/Population) * 100
FROM #PercentPopVaccinated


-- Create Views to Store Data For Later Visualizations

Create View PercentPopVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vax.new_vaccinations, 
	SUM(cast(vax.new_vaccinations as int)) OVER (Partition By dea.Location Order By dea.location, dea.date)
	as Rolling_Vax_Count
FROM PortfolioProject..CovidDeaths dea 
Join PortfolioProject..CovidVaccinations vax
	On dea.location = vax.location 
	and dea.date = vax.date
where dea.continent is not null
--order by 2,3


Create View Infection_Rate_By_Country as
Select Location, Population, MAX(total_cases)as Max_Infection_Count, Max((total_cases/Population)) * 100 as Percent_Pop_Infected
FROM PortfolioProject..CovidDeaths
Group By Location, Population
--ORDER BY Percent_Pop_Infected desc


