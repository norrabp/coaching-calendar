import { useUser } from "@context/UserContext";

const StudentHome: React.FC = () => {
    const { user } = useUser();
    return (
        <div>
            <h1>Student Home</h1>
            <p>Welcome, {user?.username}!</p>
        </div>
    );
};

export default StudentHome;