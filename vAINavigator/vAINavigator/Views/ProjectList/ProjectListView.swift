import SwiftUI
import SwiftData

struct ProjectListView: View {

    @Environment(\.modelContext) private var modelContext
    @Environment(HealthKitService.self) private var healthKit

    @Query(sort: [SortDescriptor(\Project.createdAt, order: .reverse)])
    private var projects: [Project]

    @State private var viewModel = ProjectListViewModel()
    @State private var showNewProject = false
    @State private var showSettings = false

    var body: some View {
        NavigationStack {
            ZStack {
                AppColor.background.ignoresSafeArea()
                content
            }
            .navigationTitle("vAI Navigator")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button { showSettings = true } label: {
                        Image(systemName: "gearshape")
                            .foregroundStyle(AppColor.textPrimary)
                    }
                    .accessibilityLabel("Settings")
                }
            }
            .overlay(alignment: .bottomTrailing) { floatingAddButton }
            .sheet(isPresented: $showNewProject) {
                NewProjectView()
            }
            .sheet(isPresented: $showSettings) {
                SettingsView()
            }
            .refreshable { await viewModel.refresh() }
            .alert(
                "Sync failed",
                isPresented: .constant(viewModel.syncError != nil),
                presenting: viewModel.syncError
            ) { _ in
                Button("OK") { viewModel.syncError = nil }
            } message: { message in
                Text(message)
            }
        }
    }

    // MARK: - Content

    @ViewBuilder
    private var content: some View {
        let filtered = viewModel.filter(projects)
        VStack(spacing: 12) {
            scopePicker
                .padding(.horizontal)
                .padding(.top, 4)

            if filtered.isEmpty {
                EmptyProjectsView(
                    scope: viewModel.scope,
                    createAction: { showNewProject = true }
                )
            } else {
                ScrollView {
                    LazyVStack(spacing: 14) {
                        ForEach(filtered) { project in
                            NavigationLink(value: project.id) {
                                ProjectCard(project: project)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 96) // room for the floating "+" button
                }
            }
        }
        .navigationDestination(for: UUID.self) { projectID in
            ProjectDetailPlaceholderView(projectID: projectID)
        }
    }

    private var scopePicker: some View {
        Picker("Scope", selection: Binding(
            get: { viewModel.scope },
            set: { viewModel.scope = $0 }
        )) {
            ForEach(ProjectListScope.allCases) { scope in
                Text(scope.label).tag(scope)
            }
        }
        .pickerStyle(.segmented)
    }

    private var floatingAddButton: some View {
        Button {
            showNewProject = true
        } label: {
            Image(systemName: "plus")
                .font(.title2.weight(.bold))
                .foregroundStyle(.white)
                .frame(width: 60, height: 60)
                .background(AppColor.primary)
                .clipShape(Circle())
                .shadow(color: .black.opacity(0.25), radius: 12, y: 6)
        }
        .padding(.trailing, 20)
        .padding(.bottom, 24)
        .accessibilityLabel("Create new project")
    }
}

// MARK: - Empty state

private struct EmptyProjectsView: View {
    let scope: ProjectListScope
    let createAction: () -> Void

    var body: some View {
        VStack(spacing: 18) {
            Spacer()
            Image(systemName: scope == .active ? "map" : "archivebox")
                .font(.system(size: 56, weight: .light))
                .foregroundStyle(AppColor.primary)
                .padding(24)
                .background(
                    Circle().fill(AppColor.primary.opacity(0.1))
                )
            Text(title)
                .font(AppFont.title2)
                .foregroundStyle(AppColor.textPrimary)
            Text(subtitle)
                .font(AppFont.body)
                .foregroundStyle(AppColor.textSecondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 32)

            if scope == .active {
                Button(action: createAction) {
                    Text("Create your first route")
                        .font(AppFont.bodyEmphasized)
                        .foregroundStyle(.white)
                        .padding(.horizontal, 28)
                        .padding(.vertical, 14)
                        .background(AppColor.primary)
                        .clipShape(Capsule())
                }
                .padding(.top, 4)
            }
            Spacer()
            Spacer()
        }
        .frame(maxWidth: .infinity)
    }

    private var title: String {
        switch scope {
        case .active: return "Walk your way somewhere."
        case .archived: return "No archived routes."
        }
    }

    private var subtitle: String {
        switch scope {
        case .active:
            return "Pick a destination and every hike, walk, and run you log will carry you toward it."
        case .archived:
            return "Routes you've completed or set aside will appear here."
        }
    }
}

// MARK: - Detail placeholder (session 1)

private struct ProjectDetailPlaceholderView: View {
    let projectID: UUID

    var body: some View {
        ZStack {
            AppColor.background.ignoresSafeArea()
            VStack(spacing: 12) {
                Image(systemName: "map")
                    .font(.system(size: 48, weight: .light))
                    .foregroundStyle(AppColor.primary)
                Text("Project detail")
                    .font(AppFont.title2)
                Text("Map rendering ships in a subsequent session.")
                    .font(AppFont.body)
                    .foregroundStyle(AppColor.textSecondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 32)
            }
        }
        .navigationTitle("Route")
        .navigationBarTitleDisplayMode(.inline)
    }
}

#Preview("Empty") {
    ProjectListView()
        .modelContainer(for: [Project.self, Workout.self], inMemory: true)
        .environment(HealthKitService.shared)
}
